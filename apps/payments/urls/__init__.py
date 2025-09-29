from django.urls import include, path

app_name = 'payments'

urlpatterns = [
    path('gateways/', include('apps.payments.urls.gateways')),
    path('results/', include('apps.payments.urls.results')),
]
