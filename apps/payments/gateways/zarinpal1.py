from typing import Dict, Optional
import requests
from requests.exceptions import RequestException
from decouple import config
from django.core.exceptions import ImproperlyConfigured
from ..exceptions import (
    PaymentGatewayConnectionError,
    PaymentGatewayInvalidResponse,
    PaymentGatewayRejectedError,
    ZarinpalError,
    ZarinpalInvalidMerchantError,
    PaymentVerificationFailed
)
from .base import BasePaymentGateway


class ZarinpalGateway(BasePaymentGateway):
    """
    درگاه پرداخت زرین‌پال با قابلیت‌های:
    - شروع تراکنش
    - تأیید پرداخت
    - مدیریت خطاهای تخصصی زرین‌پال
    """

    BASE_URL = config('ZARINPAL_BASE_URL')
    SANDBOX_URL = ('ZARINPAL_SANDBOX_URL')

    class StatusCodes:
        SUCCESS = 100
        INVALID_MERCHANT = -51
        DUPLICATE_TRANSACTION = -54
        INVALID_IP = -56
        INVALID_OPERATION = -57

    def __init__(self, sandbox=False, timeout=10):
        """
        مقداردهی اولیه درگاه

        Args:
            sandbox: حالت تستی (پیش‌فرض: False)
            timeout: زمان انتظار برای پاسخ (ثانیه)
        """
        self.sandbox = sandbox
        self.timeout = timeout
        self.merchant_id = config('ZARINPAL_MERCHANT_ID', default='')

        if not self.merchant_id:
            raise ImproperlyConfigured(
                "ZARINPAL_MERCHANT_ID در تنظیمات تعریف نشده است")

    def _get_base_url(self):
        """تعیین آدرس API براساس حالت تستی"""
        return self.SANDBOX_URL if self.sandbox else self.BASE_URL

    def _validate_response(self, response: requests.Response) -> Dict:
        """
        اعتبارسنجی پاسخ دریافتی از زرین‌پال

        Args:
            response: شیء پاسخ دریافتی

        Returns:
            dict: داده‌های معتبر شده

        Raises:
            PaymentGatewayConnectionError: خطاهای ارتباطی
            PaymentGatewayInvalidResponse: پاسخ نامعتبر
            PaymentGatewayRejectedError: خطای درگاه
            ZarinpalError: خطاهای اختصاصی زرین‌پال
        """
        try:
            response.raise_for_status()
            response_data = response.json()

            if not isinstance(response_data, dict):
                raise PaymentGatewayInvalidResponse(
                    "پاسخ درگاه ساختار نامعتبر دارد",
                    response_data=response.text
                )

            # بررسی خطاهای سطح درگاه
            if response_data.get('errors'):
                error = response_data['errors'][0]
                error_code = error.get('code')

                if error_code == self.StatusCodes.INVALID_MERCHANT:
                    raise ZarinpalInvalidMerchantError()
                elif error_code == self.StatusCodes.DUPLICATE_TRANSACTION:
                    raise ZarinpalError(
                        "تراکنش تکراری است",
                        error_code=error_code
                    )
                else:
                    raise PaymentGatewayRejectedError(
                        gateway_code=error_code,
                        gateway_message=error.get(
                            'message', 'خطای نامشخص از زرین‌پال')
                    )

            return response_data.get('data', {})

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 502:
                raise PaymentGatewayConnectionError(
                    "سرور زرین‌پال پاسخگو نیست")
            elif response.status_code == 401:
                raise ZarinpalInvalidMerchantError()
            else:
                raise PaymentGatewayConnectionError(
                    f"خطای HTTP {response.status_code}",
                    status_code=response.status_code
                )

        except ValueError as json_err:
            raise PaymentGatewayInvalidResponse(
                "پاسخ درگاه قابل پردازش نیست",
                response_data=response.text
            )

    def request_payment(
        self,
        amount: int,
        callback_url: str,
        description: str = "پرداخت آنلاین",
        metadata: dict = None
    ) -> dict:
        """
        ایجاد درخواست پرداخت جدید

        Args:
            amount: مبلغ به ریال
            callback_url: آدرس بازگشت
            description: توضیحات تراکنش
            metadata: داده‌های متا

        Returns:
            dict: {
                'success': bool,
                'payment_url': str,
                'authority': str,
                'fee': int
            }

        Raises:
            PaymentGatewayError: انواع خطاهای پرداخت
        """
        payload = {
            'merchant_id': self.merchant_id,
            'amount': amount,
            'callback_url': callback_url,
            'description': description,
            'metadata': metadata or {}
        }

        try:
            response = requests.post(
                f"{self._get_base_url()}/payment/request.json",
                json=payload,
                timeout=self.timeout
            )

            response_data = self._validate_response(response)

            if response_data.get('code') != self.StatusCodes.SUCCESS:
                raise PaymentGatewayRejectedError(
                    gateway_code=response_data['code'],
                    gateway_message="درخواست پرداخت رد شد"
                )

            return {
                'success': True,
                'payment_url': f"{self._get_base_url()}/StartPay/{response_data['authority']}",
                'authority': response_data['authority'],
                'fee': response_data.get('fee', 0)
            }

        except RequestException as req_err:
            raise PaymentGatewayConnectionError(
                f"خطا در ارتباط با زرین‌پال: {str(req_err)}"
            )

    def verify_payment(
        self,
        authority: str,
        amount: int
    ) -> dict:
        """
        تأیید پرداخت انجام شده

        Args:
            authority: کد مرجع تراکنش
            amount: مبلغ به ریال

        Returns:
            dict: {
                'success': bool,
                'ref_id': str,
                'card_pan': str,
                'fee': int
            }

        Raises:
            PaymentVerificationFailed: خطای تأیید پرداخت
            PaymentGatewayError: سایر خطاها
        """
        payload = {
            'merchant_id': self.merchant_id,
            'authority': authority,
            'amount': amount
        }

        try:
            response = requests.post(
                f"{self._get_base_url()}/payment/verify.json",
                json=payload,
                timeout=self.timeout
            )

            response_data = self._validate_response(response)

            if response_data.get('code') != self.StatusCodes.SUCCESS:
                raise PaymentVerificationFailed(
                    f"تأیید پرداخت ناموفق (کد: {response_data['code']})",
                    ref_id=response_data.get('ref_id'),
                    amount=amount
                )

            return {
                'success': True,
                'ref_id': str(response_data['ref_id']),
                'card_pan': response_data.get('card_pan', ''),
                'fee': response_data.get('fee', 0),
                'transaction_id': authority
            }

        except RequestException as req_err:
            raise PaymentGatewayConnectionError(
                f"خطا در تأیید پرداخت: {str(req_err)}"
            )

    def get_gateway_name(self) -> str:
        """نام رسمی درگاه"""
        return 'zarinpal' + ('_sandbox' if self.sandbox else '')
