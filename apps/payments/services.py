from django.conf import settings
from typing import Dict, Type
from .exceptions import PaymentGatewayNotSupported
from .gateways.base import BasePaymentGateway


class PaymentService:
    """
    سرویس مرکزی مدیریت درگاه‌های پرداخت با قابلیت:
    - انتخاب پویای درگاه پرداخت
    - مدیریت یکپارچه خطاها
    - پیکربندی متمرکز
    """

    _gateways: Dict[str, Type[BasePaymentGateway]] = {}
    _initialized = False

    @classmethod
    def _init_gateways(cls):
        """بارگذاری پویای درگاه‌های پرداخت از تنظیمات"""
        if cls._initialized:
            return

        # ثبت درگاه‌های فعال از تنظیمات
        for gateway in settings.PAYMENT_GATEWAYS:
            if not gateway.get('enabled'):
                continue
            try:
                module = __import__(
                    f"apps.payments.gateways.{gateway['module']}",
                    fromlist=[gateway['class']]
                )
                gateway_class = getattr(module, gateway['class'])
                cls._gateways[gateway['name']] = gateway_class
            except (ImportError, AttributeError) as e:
                raise ImportError(
                    f"خطا در بارگذاری درگاه {gateway['name']}: {str(e)}"
                ) from e

        cls._initialized = True

    @classmethod
    def get_gateway(cls, gateway_name: str) -> BasePaymentGateway:
        """
        ایجاد نمونه درگاه پرداخت مورد نظر

        Args:
            gateway_name: نام درگاه (مثلاً 'zarinpal')

        Returns:
            نمونه ساخته شده از درگاه پرداخت

        Raises:
            PaymentGatewayNotSupported: اگر درگاه پشتیبانی نشود
        """
        cls._init_gateways()

        gateway_class = cls._gateways.get(gateway_name.lower())
        if not gateway_class:
            raise PaymentGatewayNotSupported(
                f"درگاه پرداخت {gateway_name} پشتیبانی نمی‌شود. "
                f"درگاه‌های موجود: {', '.join(cls._gateways.keys())}"
            )

        return gateway_class()

    @classmethod
    def get_active_gateways(cls) -> Dict[str, str]:
        """
        لیست درگاه‌های فعال با نام و عنوان نمایشی

        Returns:
            dict: {'zarinpal': 'زرین‌پال', 'mellat': 'ملت'}
        """
        cls._init_gateways()
        return {
            name: gateway_class.display_name
            for name, gateway_class in cls._gateways.items()
        }
