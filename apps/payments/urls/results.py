from django.urls import path
from apps.payments.views.results.success import PaymentSuccessView
from apps.payments.views.results.failed import PaymentFailedView

app_name = 'results'

urlpatterns = [
    path(
        'success/<int:pk>/',
        PaymentSuccessView.as_view(),
        name='success'
    ),
    path(
        'failed/<str:error>/',
        PaymentFailedView.as_view(),
        name='failled'
    )
]
