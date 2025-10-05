from django.urls import path
from . import views
from .views import (
    anbar_list_view,
    anbar_save
)

app_name = 'anbar'


urlpatterns = [
    path('anbar-list/', anbar_list_view, name='anbar_list'),
    path('anbar-save/', anbar_save, name='anbar_save'),
]