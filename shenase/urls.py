from django.urls import path
from . import views
from .views import (
    ShenaseListView,
    ShenaseCreateView,
    ShenaseDataView,
    ShenaseTransactionsView,
    ShenaseOneDataView
)

app_name = 'shenase'


urlpatterns = [
    # لیست سرفصل‌ها
    path('list/', ShenaseListView.as_view(), name='shenase_list'),
    path('add/', ShenaseCreateView.as_view(), name='shenase_add'),
    path('in_trasactions/', ShenaseTransactionsView.as_view(), name='shenase_in_trasactions'), 
    path("upload/", views.upload_file, name="upload_file"),
    path("save-shenase/", views.save_shenase, name="save_shenase"),

    
    
    # JSON API
    path('json/', ShenaseDataView.as_view(), name='shenase_json'),                    
    path('json/<str:type>/', ShenaseDataView.as_view(), name='shenase_json_id'), 
    path('json/one/<str:id>/', ShenaseOneDataView.as_view(), name='shenase_json_id_one'), 

]