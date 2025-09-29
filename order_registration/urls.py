from django.urls import path

from .views import (
    MainDataCreateView,
    CustomsAndShippingCreateView,
    ShippingJsonList,
    EntranceEdgeJsonList,
    CustomJsonList,
    FinancialCreateView,
    WareCreateView,
    BankBranchJsonView,
    WareListView,
    WareDeleteView,
    MainDataListView,
    MainDataUploadDocumentView,
    MainDataDetailView,
    MainDataStatusUpdateView,
    MainDataUpdateView,
    CustomsAndShippingUpdateView,
    FinancialUpdateView,
    CurrencySupplyJsonListView,
    WareUpdateView,
    WareBulkDeleteView,
    generate_order_registration_pdf,
    PayView,
)

app_name = 'order_registration'

urlpatterns = [
    path('create-main-data/', MainDataCreateView.as_view(), name='create_main_data'),
    path('create-cusotms-and-shipping/<int:main_data_id>/', CustomsAndShippingCreateView.as_view(),
         name="create_customs_and_shipping"),
    path('shipping-json-list/<int:incoterms_id>/', ShippingJsonList.as_view(),
         name="shipping_json_list"),
    path('entrance-json-list/<int:shipping_type_id>/', EntranceEdgeJsonList.as_view(),
         name="shipping_json_list"),
    path('entrance-json-list/', EntranceEdgeJsonList.as_view(),
         name="shipping_json_list"),
    path('custom-json-list/<int:entrance_id>/', CustomJsonList.as_view(),
         name="custom_json_list"),
    path('custom-json-list/', CustomJsonList.as_view(),
         name="custom_json_list"),
    path('create-financial/<int:main_data_id>/',
         FinancialCreateView.as_view(), name='create_financial'),
    path('ware-list/<int:main_data_id>/',
         WareListView.as_view(), name='ware_list'),
    path('create-ware/<int:main_data_id>/',
         WareCreateView.as_view(), name='create_ware'),
    path('bank-branch-json/<int:bank_id>/',
         BankBranchJsonView.as_view(), name='bank_branch_json'),
    path('delete-ware/<int:pk>', WareDeleteView.as_view(), name='delete_ware'),
    path('main-data-list', MainDataListView.as_view(), name='main_data_list'),
    path('upload-document/<int:pk>/',
         MainDataUploadDocumentView.as_view(), name='upload_document'),
    path('detail/<int:pk>/', MainDataDetailView.as_view(), name="detail"),
    path('main-data-update-status/<int:main_data_id>/',
         MainDataStatusUpdateView.as_view(), name="update_status"),
    path('main-data-update-status/<int:main_data_id>/<str:operation>/',
         MainDataStatusUpdateView.as_view(), name="update_status_with_operation"),
    path('update-main-data/<int:pk>/',
         MainDataUpdateView.as_view(),
         name="update_main_data"
         ),
    path(
        'update-shipping-and-custom/<int:pk>/',
        CustomsAndShippingUpdateView.as_view(),
        name='update_customs_and_shipping'
    ),
    path(
        'update-financial/<int:pk>/',
        FinancialUpdateView.as_view(),
        name="update_financial"
    ),
    path(
        'currency-supply-json-list/<str:currency_operation_type>',
        CurrencySupplyJsonListView.as_view(),
        name='currency-supply-json-list'
    ),
    path(
        'update-ware/<int:pk>',
        WareUpdateView.as_view(),
        name='update_ware'
    ),
    path('ware-bulk-delete',
         WareBulkDeleteView.as_view(),
         name="ware_bulk_delete"
         ),
    path(
        'generate-pdf/<int:pk>',
        generate_order_registration_pdf,
        name="generate_pdf"
    ),
    path('pay',
         PayView.as_view(),
         name='pay')



]
