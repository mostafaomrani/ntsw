from django.urls import path, include
from apps.payments.views.gateways.gateways_list import SelectPaymentView
from apps.payments.views.gateways.zarinpal import ZarinpalPaymentView

urlpatterns = [
    path(
        'zarinpal/pay/',
        ZarinpalPaymentView.as_view(),
        name='zarinpal_payment'
    ),
    path(
        'zarinpal/verify/',
        ZarinpalPaymentView.as_view(verify=True),
        name='zarinpal_verify'
    ),
    path(
        '',
        SelectPaymentView.as_view(),
        name='payments'
    ),
]
