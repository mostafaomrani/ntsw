from django.contrib import admin
from .models import BusinessCard, CompanyBase


@admin.register(BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyBase)
class CompanyBaseAdmin(admin.ModelAdmin):
    pass
