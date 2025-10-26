from django.urls import path

from .views import BusinessCardListView, BusinessCardCreateView, CompanyBaseCreateView, ResellerIntroducingView,get_address_by_postal_code
from . import views

app_name = 'upload_qualifications'

urlpatterns = [
    path("business-cards/", BusinessCardListView.as_view(), name="business_cards"),
    path("introducing-reseller/", ResellerIntroducingView.as_view(), name="introducing_reseller"),
    path('create-business-card', BusinessCardCreateView.as_view(),name="create_business_card"),
    path('create-business-card/<str:active>', BusinessCardCreateView.as_view(),name="create_business_card"),
    path('create-company-base', CompanyBaseCreateView.as_view(), name="create_company_base"),
    path("save_trader_role/", views.save_trader_role, name="save_trader_role"),
    path("get-address-by-postal-code/", views.get_address_by_postal_code, name="get_address_by_postal_code"), 
    path("delete-trader-role/", views.delete_trader_role, name="delete_trader_role"),
]
