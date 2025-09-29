import requests
from requests.exceptions import RequestException
from typing import Dict, Optional
from decouple import config
from apps.payments.exceptions import (
    PaymentGatewayConnectionError,
    PaymentGatewayInvalidResponse,
    PaymentGatewayRejectedError,
    PaymentVerificationFailed,
)

from .base import BasePaymentGateway


class ZarinpalGateway(BasePaymentGateway):
    BASE_URL = config('ZARINPAL_BASE_URL')

    def request_payment(
        self,
        amount: int,
        callback_url: str,
        metadata: Optional[Dict] = None,
        currency: str = 'IRT',
        timeout: int = 10
    ) -> Dict:
        """
        درخواست پرداخت به زرین‌پال

        Args:
            amount: مبلغ به ریال
            callback_url: آدرس بازگشت
            metadata: داده‌های متا اختیاری
            timeout: زمان انتظار برای پاسخ (ثانیه)

        Returns:
            dict: نتیجه پرداخت با کلیدهای success, payment_url, transaction_id

        Raises:
            PaymentGatewayConnectionError: خطا در ارتباط با سرور
            PaymentGatewayInvalidResponse: پاسخ نامعتبر از درگاه
            PaymentGatewayRejectedError: رد درخواست توسط درگاه
        """
        if metadata is None:
            metadata = {}
        payload = {
            'merchant_id': config('ZARINPAL_MERCHANT_ID'),
            'amount': amount,
            'callback_url': callback_url,
            'description': metadata.get('description', ''),
            'metadata': metadata,
            'currency': currency,
        }
        try:
            response = requests.post(
                f"{self.BASE_URL}v4/payment/request.json",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()

            response_data = response.json()

            # بررسی ساختار پاسخ
            if not all(key in response_data for key in ['data', 'errors']):
                raise PaymentGatewayInvalidResponse(
                    "پاسخ درگاه ساختار نامعتبر دارد")
            # مدیریت خطاهای درگاه
            if response_data['errors']:
                error_code = response_data['errors'].get('code', -1)
                error_message = response_data['errors'].get(
                    'message', 'خطای نامشخص')
                raise PaymentGatewayRejectedError(
                    f"درگاه پرداخت خطا داد (کد {error_code}): {error_message}"
                )

            # بررسی داده‌های ضروری
            if 'authority' not in response_data['data'] or 'code' not in response_data['data']:
                raise PaymentGatewayInvalidResponse(
                    "داده‌های ضروری در پاسخ وجود ندارد")

            # بررسی کد پاسخ
            if response_data['data']['code'] != 100:
                raise PaymentGatewayRejectedError(
                    f"درخواست پرداخت رد شد (کد {response_data['data']['code']})"
                )

            return {
                'success': True,
                'payment_url': f"{self.BASE_URL}StartPay/{response_data['data']['authority']}",
                'transaction_id': response_data['data']['authority'],
                'fee': response_data['data'].get('fee', 0),  # کارمزد اختیاری
                'authority': response_data['data']['authority'],
            }

        except RequestException as e:
            raise PaymentGatewayConnectionError(
                f"خطا در ارتباط با زرین‌پال: {str(e)}"
            ) from e
        except ValueError as e:
            raise PaymentGatewayInvalidResponse(
                "پاسخ درگاه قابل پردازش نیست (JSON نامعتبر)"
            ) from e

    def verify_payment(
        self,
        authority: str,
        amount: int,
        timeout: int = 10
    ) -> Dict:
        """
        تأیید پرداخت در زرین‌پال با مدیریت کامل خطاها

        Args:
            authority: کد مرجع تراکنش
            amount: مبلغ به ریال
            timeout: زمان انتظار برای پاسخ (ثانیه)

        Returns:
            dict: نتیجه تأیید پرداخت با کلیدهای:
                - success (bool)
                - ref_id (str): شماره پیگیری
                - fee (int): کارمزد
                - card_pan (str): شماره کارت ماسک شده
                - message (str): پیام پاسخ

        Raises:
            PaymentGatewayConnectionError: خطاهای ارتباطی/اتصال
            PaymentGatewayTimeoutError: خطاهای timeout
            PaymentGatewayInvalidResponse: پاسخ نامعتبر از درگاه
            PaymentVerificationFailed: تأیید پرداخت ناموفق
        """
        payload = {
            'merchant_id': config('ZARINPAL_MERCHANT_ID'),
            'authority': authority,
            'amount': amount
        }

        try:
            # ارسال درخواست تأیید
            response = requests.post(
                f"{self.BASE_URL}v4/payment/verify.json",
                json=payload,
                timeout=timeout
            )

            # مدیریت خطاهای HTTP
            try:
                if response.status_code != 200:
                    error_message = f"کد وضعیت HTTP نامعتبر: {response.status_code}"
                    try:
                        error_data = response.json()
                        if isinstance(error_data, dict):
                            if 'errors' in error_data and isinstance(error_data['errors'], dict):
                                error_message = error_data['errors'].get(
                                    'message', error_message)
                            else:
                                error_message = error_data.get(
                                    'message', error_message)
                    except (ValueError, requests.JSONDecodeError):
                        pass

                    if 400 <= response.status_code < 500:
                        raise PaymentVerificationFailed(error_message)
                    else:
                        raise PaymentGatewayConnectionError(error_message)

                # پردازش پاسخ موفق
                response_data = response.json()

            except requests.JSONDecodeError as e:
                raise PaymentGatewayInvalidResponse(
                    "پاسخ درگاه قابل پردازش نیست (JSON نامعتبر)"
                ) from e
            except ValueError as e:
                raise PaymentGatewayInvalidResponse(
                    "پاسخ درگاه قابل پردازش نیست (داده نامعتبر)"
                ) from e

            # بررسی ساختار پاسخ
            if not isinstance(response_data, dict):
                raise PaymentGatewayInvalidResponse(
                    "فرمت پاسخ درگاه نامعتبر است"
                )

            # بررسی وجود کلیدهای اصلی
            if 'data' not in response_data or not isinstance(response_data.get('data'), dict):
                raise PaymentGatewayInvalidResponse(
                    "ساختار پاسخ درگاه نامعتبر است (فیلد data یافت نشد)"
                )

            if 'errors' not in response_data:
                raise PaymentGatewayInvalidResponse(
                    "ساختار پاسخ درگاه نامعتبر است (فیلد errors یافت نشد)"
                )

            # مدیریت خطاهای اختصاصی زرین‌پال
            if response_data['errors'] and isinstance(response_data['errors'], dict):
                error_code = response_data['errors'].get('code', 'نامشخص')
                error_message = response_data['errors'].get(
                    'message', 'خطای نامشخص در تأیید پرداخت')
                raise PaymentVerificationFailed(
                    f"کد خطا: {error_code} - {error_message}"
                )

            # بررسی داده‌های ضروری
            required_data_keys = ['code', 'ref_id']
            if not all(key in response_data['data'] for key in required_data_keys):
                raise PaymentGatewayInvalidResponse(
                    "داده‌های ضروری در پاسخ وجود ندارد"
                )

            # بررسی کد پاسخ (100 و 101 کدهای موفقیت‌آمیز هستند)
            if response_data['data']['code'] not in (100, 101):
                raise PaymentVerificationFailed(
                    f"تأیید پرداخت ناموفق (کد: {response_data['data']['code']})"
                )

            # پرداخت موفق
            return {
                'success': True,
                'ref_id': str(response_data['data']['ref_id']),
                'fee': response_data['data'].get('fee', 0),
                'card_pan': response_data['data'].get('card_pan', ''),
                'message': response_data['data'].get('message', 'پرداخت موفق')
            }

        except requests.ConnectTimeout as e:
            raise PaymentGatewayTimeoutError(
                "زمان اتصال به درگاه پرداخت به پایان رسید"
            ) from e
        except requests.ReadTimeout as e:
            raise PaymentGatewayTimeoutError(
                "زمان خواندن پاسخ از درگاه پرداخت به پایان رسید"
            ) from e
        except requests.Timeout as e:
            raise PaymentGatewayTimeoutError(
                "زمان درخواست به درگاه پرداخت به پایان رسید"
            ) from e
        except requests.ConnectionError as e:
            raise PaymentGatewayConnectionError(
                "خطا در اتصال به درگاه پرداخت"
            ) from e
        except requests.HTTPError as e:
            raise PaymentGatewayConnectionError(
                f"خطای HTTP در ارتباط با درگاه پرداخت: {str(e)}"
            ) from e
        except requests.RequestException as e:
            raise PaymentGatewayConnectionError(
                f"خطای عمومی در ارتباط با درگاه پرداخت: {str(e)}"
            ) from e

    def get_gateway_name(self) -> str:
        """
        نام رسمی درگاه پرداخت را برمی‌گرداند

        Returns:
            str: نام منحصربه‌فرد درگاه با فرمت استاندارد

        نکات:
            - نام باید به صورت snake_case باشد
            - فقط شامل حروف کوچک و underline
            - بدون فاصله یا کاراکترهای خاص
        """
        return 'zarinpal'
