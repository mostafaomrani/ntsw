from django.urls import path
from .views import BaseRoleView


app_name = 'dashboard'

urlpatterns = [
    path('role/', BaseRoleView.as_view(), name='base_role_dashboard'),
]
