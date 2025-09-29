from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from apps.payments.services import PaymentService
from apps.payments.exceptions import (
    PaymentValidationError,
    PaymentGatewayError,
    PaymentVerificationFailed
)
import logging

logger = logging.getLogger(__name__)


class BasePaymentView(View):
    verify = False
    """
    کلاس پایه برای پرداخت‌های آنلاین با ویژگی‌های:
    - استفاده از PaymentService برای مدیریت درگاه‌ها
    - پشتیبانی از چندین درگاه پرداخت
    - مدیریت چرخه کامل پرداخت
    - خطاهای استاندارد
    """

    gateway_name = None  # باید در کلاس فرزند تعیین شود (مثلاً 'zarinpal')
    amount_field = 'amount'
    template_name = 'payment/payment_form.html'
    verify_template_name = 'payment/verify.html'
    error_template_name = 'payment/error.html'

    # ==================== متدهای اصلی ====================
    def get_payment_amount(self, request) -> int:
        """
        دریافت مبلغ پرداخت (باید در کلاس فرزند پیاده‌سازی شود)

        Raises:
            PaymentValidationError: اگر مبلغ نامعتبر باشد
        """
        raise NotImplementedError("متد get_payment_amount باید پیاده‌سازی شود")

    def get_payment_metadata(self, request) -> dict:
        """دریافت متادیتای پرداخت (اختیاری)"""
        return {}

    def get_callback_url(self, request) -> str:
        """آدرس بازگشت از درگاه"""
        return request.build_absolute_uri(f'/payments/gateways/{self.gateway_name}/verify/')

    def on_payment_success(self, request, payment_result: dict):
        """
        پرداخت موفق (باید در کلاس فرزند پیاده‌سازی شود)

        Args:
            payment_result: {
                'ref_id': str,       # شماره پیگیری
                'amount': int,       # مبلغ
                'gateway': str,      # نام درگاه
                'metadata': dict     # متادیتای پرداخت
            }
        """
        raise NotImplementedError("متد on_payment_success باید پیاده‌سازی شود")

    def on_payment_failure(self, request, error: Exception):
        """پرداخت ناموفق (اختیاری)"""
        pass

    # ==================== متدهای پرداخت ====================
    def get_gateway(self):
        """دریافت درگاه پرداخت از PaymentService"""
        if not self.gateway_name:
            raise ImproperlyConfigured("gateway_name باید تعیین شود")

        try:
            return PaymentService.get_gateway(self.gateway_name)
        except Exception as e:
            logger.error(f"خطا در دریافت درگاه پرداخت: {str(e)}")
            raise PaymentGatewayError(f"خطا در سیستم پرداخت: {str(e)}")

    def initiate_payment(self, request):
        """شروع فرآیند پرداخت"""
        try:
            amount = self.get_payment_amount(request)
            metadata = self.get_payment_metadata(request)
            callback_url = self.get_callback_url(request)

            gateway = self.get_gateway()
            result = gateway.request_payment(
                amount=amount,
                callback_url=callback_url,
                metadata=metadata
            )

            # ذخیره اطلاعات پرداخت در session
            request.session['payment_data'] = {
                'gateway': self.gateway_name,
                'amount': amount,
                'authority': result.get('authority'),
                'metadata': metadata
            }
            request.session.modified = True

            return result['payment_url']

        except Exception as e:
            logger.error(f"خطا در شروع پرداخت: {str(e)}")
            raise

    def verify_payment(self, request):
        """تأیید پرداخت"""
        try:
            payment_data = request.session.get('payment_data', {})

            if payment_data.get('gateway') != self.gateway_name:
                raise PaymentVerificationFailed("ناسازگاری درگاه پرداخت")

            gateway = self.get_gateway()
            verification = gateway.verify_payment(
                authority=payment_data['authority'],
                amount=payment_data['amount']
            )

            # پاکسازی session
            if 'payment_data' in request.session:
                del request.session['payment_data']
            return {
                'ref_id': verification['ref_id'],
                'amount': payment_data['amount'],
                'gateway': self.gateway_name,
                'metadata': payment_data.get('metadata', {}),
                'transaction_id': payment_data['authority'],
            }

        except Exception as e:
            logger.error(f"خطا در تأیید پرداخت: {str(e)}")
            raise
    # ==================== متدهای ویو ====================

    def get(self, request, *args, **kwargs):
        """نمایش فرم پرداخت"""
        if getattr(self, 'verify', False):
            return self.handle_verify(request)

        return self.render_to_response({
            'gateway_name': self.gateway_name,
            'amount_field': self.amount_field
        })

    def post(self, request, *args, **kwargs):
        """درخواست پرداخت"""
        try:
            payment_url = self.initiate_payment(request)
            return redirect(payment_url)

        except Exception as e:
            return self.handle_error(request, e)

    def handle_verify(self, request):
        """مدیریت بازگشت از درگاه"""
        try:
            payment_result = self.verify_payment(request)
            return self.on_payment_success(request, payment_result)

        except Exception as e:
            return self.handle_error(request, e)

    def handle_error(self, request, error):
        """مدیریت خطاها"""
        return self.on_payment_failure(request, error)
