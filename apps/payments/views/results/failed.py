from django.views import View
from django.shortcuts import get_object_or_404, render
from apps.payments.models import Payment


class PaymentFailedView(View):
    template_name = 'payments/results/failed.html'

    def get(self, request, error):

        context = {
            'error': error,
        }
        return render(request, self.template_name, context)
