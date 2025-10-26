from django.urls import path
from . import views
from .views import (
    ProductEzharListView,
    ProductAmarTolidMonthListView,
    ProductEzharBaravadKalaListView,
    ProductEzharTolidKalaListView,
    ProductSabtAmarEshteghalListView
)

app_name = 'production_operations'


urlpatterns = [
    path('list/', ProductEzharListView.as_view(), name='product_ezhar_list'),
    path('amar-month-list/', ProductAmarTolidMonthListView.as_view(), name='product_amar_month_list'),
    path('ezhar-baravad-kala/', ProductEzharBaravadKalaListView.as_view(), name='product_ezhar_baravad_kala'),
    path('ezhar-tolid-kala-steps/', ProductEzharTolidKalaListView.as_view(), name='product_ezhar_tolid_kala'),
    path('sabt-amar-eshteghal-steps/', ProductSabtAmarEshteghalListView.as_view(), name='sabt_amar_eshteghal'),
]