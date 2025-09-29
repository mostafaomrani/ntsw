from django.views import View
from django.shortcuts import render
from django.conf import settings


class SelectPaymentView(View):
    def get(self, request):
        context = {
            'payments': settings.PAYMENT_GATEWAYS
        }
        return render(request, 'payments/select_gateway.html', context)
