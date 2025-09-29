from django.urls import path
from . import views
from .views import (
    ForeintradeInputListView,
    ForeintradeOutputListView,
    ForeintradeManageKalaListView,
    ForeintradeVoroodListView,
    ForeintradeKhoroojListView,
    ForeintradeExcelModiriatListView,
    ForeintradeElectronicFactorListView,
    ForeintradeMaliatSooratHesabListView,
    ForeintradeVaziatAmalkardListView,
    ForeintradeBoorsKalaListView,
    ForeintradeCreateView
)

app_name = 'foreintrade'


urlpatterns = [
    path('input-list/', ForeintradeInputListView.as_view(), name='foreintrade_input_list'),
    path('output-list/', ForeintradeOutputListView.as_view(), name='foreintrade_output_list'),
    path('managment-kala/', ForeintradeManageKalaListView.as_view(), name='foreintrade_manage_list'),
    path('ezhar-vorood-kala/', ForeintradeVoroodListView.as_view(), name='foreintrade_vorood_kala'),
    path('ezhar-khorooj-kala/', ForeintradeKhoroojListView.as_view(), name='foreintrade_khorooj_kala'),
    path('modiriat-asnad-excel/', ForeintradeExcelModiriatListView.as_view(), name='foreintrade_asand_excel'),
    path('electronic-factors/', ForeintradeElectronicFactorListView.as_view(), name='foreintrade_electronic_factor'),
    path('maliat-sorathesab/', ForeintradeMaliatSooratHesabListView.as_view(), name='foreintrade_maliat_soorathesab'),
    path('vaziat-amalkard/', ForeintradeVaziatAmalkardListView.as_view(), name='foreintrade_vaziat_amalkard'),
    path('boors-kala/', ForeintradeBoorsKalaListView.as_view(), name='foreintrade_boors_kala'),
    path('add/', ForeintradeCreateView.as_view(), name='shenase_add'),   
]