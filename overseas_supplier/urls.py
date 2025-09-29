from django.urls import path
from .views import (
    OverSeasSuplierListView,
    PersonCreateView,
    CompanyCreateView,
    PersonJsonListView,
    CompanyJsonListView,
    PersonJson,
    CompanyJson,
    PersonJsonByIdentifer,
    CompanyJsonByIdentifier,

)

app_name = 'supplier'

urlpatterns = [
    path('', OverSeasSuplierListView.as_view(), name='supplier_list'),
    path('create-person', PersonCreateView.as_view(), name='create_person'),
    path('create-company', CompanyCreateView.as_view(), name='create_company'),
    path('person-json-list', PersonJsonListView.as_view(), name='person_json_list'),
    path('person-json/<int:id>', PersonJson.as_view(), name='person_json'),
    path(
        'person-json-by-identifier/<int:identifier>',
        PersonJsonByIdentifer.as_view(),
        name='person_json_identifier'
    ),
    path('company-json-list', CompanyJsonListView.as_view(),
         name='company_json_list'),
    path('company-json/<int:company_id>',
         CompanyJson.as_view(), name='company_json'),
    path(
        'company-json-by-identifier/<int:identifier>',
        CompanyJsonByIdentifier.as_view(),
        name='company_json_identifier'
    ),

]
