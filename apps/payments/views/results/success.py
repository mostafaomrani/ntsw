from django.views import View
from django.shortcuts import get_object_or_404, render
from apps.payments.models import Payment


class PaymentSuccessView(View):
    template_name = 'payments/results/success.html'

    def get(self, request, pk):
        payment = get_object_or_404(
            Payment,
            pk=pk,
            status='success',
        )
        context = {
            'payment': payment,
        }
        return render(request, self.template_name, context)
