from django.urls import path
from . import views
from .views import (
    DocumentTradeOperationListView,
    ForeintradeOutputListView,
    ForeintradeManageKalaListView,
    AnbarItemsListView,
    ForeintradeVoroodListView,
    ForeintradeKhoroojListView,
    ForeintradeExcelModiriatListView,
    ForeintradeElectronicFactorListView,
    ForeintradeMaliatSooratHesabListView,
    ForeintradeVaziatAmalkardListView,
    ForeintradeBoorsKalaListView,
    ForeintradeCreateView,
    RegisterForeintradeKhoroojListView,
    SaveTransferView,
    ForeintradeEzharvoroodStepListView,
    CheckShenaseView,
    AddKalaView  # اضافه کردن ویوی جدید
)

app_name = 'foreintrade'

urlpatterns = [
    path('input-list/', DocumentTradeOperationListView.as_view(), name='foreintrade_input_list'),
    path('output-list/', ForeintradeOutputListView.as_view(), name='foreintrade_output_list'),
    path('managment-kala/', AnbarItemsListView.as_view(), name='foreintrade_manage_list'),
    path('ezhar-vorood-kala/', ForeintradeVoroodListView.as_view(), name='foreintrade_vorood_kala'),
    path('ezhar-vorood-kala-steps/', ForeintradeEzharvoroodStepListView.as_view(), name='product_ezhar_vorood_kala'),
    path('ezhar-khorooj-kala/', ForeintradeKhoroojListView.as_view(), name='foreintrade_khorooj_kala'),
    path('register-ezhar-khorooj-kala/', RegisterForeintradeKhoroojListView.as_view(), name='register_foreintrade_khorooj_kala'),
    path('modiriat-asnad-excel/', ForeintradeExcelModiriatListView.as_view(), name='foreintrade_asand_excel'),
    path('electronic-factors/', ForeintradeElectronicFactorListView.as_view(), name='foreintrade_electronic_factor'),
    path('maliat-sorathesab/', ForeintradeMaliatSooratHesabListView.as_view(), name='foreintrade_maliat_soorathesab'),
    path('vaziat-amalkard/', ForeintradeVaziatAmalkardListView.as_view(), name='foreintrade_vaziat_amalkard'),
    path('boors-kala/', ForeintradeBoorsKalaListView.as_view(), name='foreintrade_boors_kala'),
    path('add/', ForeintradeCreateView.as_view(), name='shenase_add'),   
    path('approve/<int:pk>/', views.approve_document, name='approve_document'),
    path('transfer/save/', SaveTransferView.as_view(), name='save_transfer'),   
    path('check-shenase/', CheckShenaseView.as_view(), name='check_shenase'),
    path('add-kala/', AddKalaView.as_view(), name='add_kala'),
]