from abc import ABC, abstractmethod
from django.conf import settings


class BasePaymentGateway(ABC):
    """
    کلاس پایه برای تمام درگاه‌های پرداخت.
    هر درگاه جدید باید این متدها را پیاده‌سازی کند.
    """

    def __init__(self):
        """مقداردهی اولیه با تنظیمات پروژه"""
        self.sandbox = getattr(settings, 'DEBUG', False)  # حالت تستی در توسعه

    @abstractmethod
    def request_payment(self, amount: int, callback_url: str) -> dict:
        """
        ارسال درخواست پرداخت به درگاه

        Args:
            amount: مبلغ به ریال
            callback_url: آدرس بازگشت از درگاه

        Returns:
            dict: پاسخ درگاه شامل {'success': bool, 'payment_url': str, 'transaction_id': str}

        Raises:
            PaymentGatewayError: در صورت خطا
        """
        pass

    @abstractmethod
    def verify_payment(self, request) -> dict:
        """
        بررسی صحت تراکنش برگشتی از درگاه

        Args:
            request: درخواست Django حاوی پارامترهای بازگشتی

        Returns:
            dict: نتیجه تأیید پرداخت {'success': bool, 'amount': int, 'ref_id': str}
        """
        pass

    @abstractmethod
    def get_gateway_name(self) -> str:
        """نام منحصربه‌فرد درگاه (مثلاً 'zarinpal')"""
        pass

    def get_redirect_html(self, payment_url: str) -> str:
        """
        متد اختیاری برای ساخت HTML ریدایرکت خودکار
        (می‌توان در درگاه‌ها Override کرد)
        """
        return f"""
        <html>
            <body>
                <script>window.location.href = "{payment_url}";</script>
            </body>
        </html>
        """
