from django.urls import path
from .views import (
    BankingListView,
    BankingCreateView,
    WithoutCurrencyTransferListView,
    WithoutCurrencyTransferCreateView,
    BankingDetailView,
    WithoutCurrencyTransferDetail,
    BankingStatusUpdate,
    WithoutCurrencyTransferStatusUpdate
)

app_name = 'currency_origin_determining'

urlpatterns = [
    path(
        'banking-list/',
        BankingListView.as_view(),
        name="banking_list"
    ),
    path(
        'create-banking/',
        BankingCreateView.as_view(),
        name="create_banking",
    ),
    path(
        'without-transfer-currency-list/',
        WithoutCurrencyTransferListView.as_view(),
        name='without_currency_transfer_list'
    ),
    path(
        'without-transfer-currency-create',
        WithoutCurrencyTransferCreateView.as_view(),
        name='without_currency_transfer_create'
    ),
    path(
        'banking-detail/<int:pk>/',
        BankingDetailView.as_view(),
        name="banking_detail"
    ),
    path('without-currency-transfer-detail/<int:pk>',
         WithoutCurrencyTransferDetail.as_view(),
         name='without_currency_transfer_detail'
         ),

    path('update-banking-status/<int:pk>',
         BankingStatusUpdate.as_view(),
         name='update_banking_status'
         ),
    path('update-without-transfer-status<int:pk>',
         WithoutCurrencyTransferStatusUpdate.as_view(),
         name="update_without_currency_status"
         )
]
