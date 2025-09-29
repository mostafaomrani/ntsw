from apps.payments.views.base import BasePaymentView
from django.shortcuts import Http404
from uuid import UUID
from apps.payments.models import Payment
from django.shortcuts import redirect
from order_registration.models import MainData
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


class ZarinpalPaymentView(BasePaymentView):
    gateway_name = 'zarinpal'

    def get_payment_amount(self, request):
        amount = 10000
        return amount

    def get_payment_metadata(self, request):
        meta_data = {}
        main_data_id = int(request.session.get('main_data_id'))
        meta_data['description'] = f'پرداخت بابت ثبت سفارش {main_data_id}'
        user = request.user
        if request.user.is_authenticated and user.mobile:
            meta_data['mobile'] = str(user.mobile)
        return meta_data

    def on_payment_success(self, request, result):
        # ذخیره پرداخت در دیتابیس
        main_data_id = int(request.session.get('main_data_id'))
        main_data = MainData.objects.get(pk=main_data_id)
        user = request.user if request.user.is_authenticated else None
        payment = Payment.objects.create(
            user=user,
            amount=result['amount'],
            ref_id=result['ref_id'],
            gateway=self.gateway_name,
            transaction_id=result['transaction_id'],
            status='success',
            meta=result['metadata'],
            order=main_data
        )

        # ریدایرکت به صفحه موفقیت
        messages.success(request, 'ثبت سفارش با موفقیت انجام شده')
        return redirect('order_registration:update_status', main_data_id=main_data_id)

    def on_payment_failure(self, request, error):
        logger.error(f'خطا در پرداخت کاربر f{request.user}: {str(error)}')
        return redirect('payments:results:failled', error=str(error))
