import requests
from requests.exceptions import RequestException
# from typing import Dict, Optional
from decouple import config
from apps.payments.exceptions import (
    PaymentGatewayConnectionError,
    PaymentGatewayInvalidResponse,
    PaymentGatewayRejectedError
)

from .base import BasePaymentGateway


class ZibalGateway(Base):
    BASE_URL = config('ZIBAL_BASE_URL')

    def request_payment(
        self,
        amount: int,
        calback_url: str,
        metadata: dict = None,
        timeout: int = 10
    ) -> dict:
        """
        درخواست پرداخت به زیبال
        Args:
            amount: مبلغ به ریال
            callback_url: آدرس بازگشت
            metadata: داده‌های متا اختیاری
            timeout: زمان انتظار برای پاسخ(ثانیه)

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
            'merchant': config('ZIBAL_MERCHANT'),
            'amount': amount,
            'calback_url': calback_url,
            'description': metadata.get('description', ''),

        }
        try:
            response = requests.post(
                f'{self.BASE_URL}request',
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            response_data = response.json()

            if not all(key in response_data for key in ['trackId', 'result', 'message']):
                raise PaymentGatewayInvalidResponse(
                    'پاسخ درگاه ساختار نا معتبر دارد'
                )

        except:
            ...
