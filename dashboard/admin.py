from django.contrib import admin
from .models import Country, Currency
from import_export.admin import ImportExportModelAdmin


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdming(ImportExportModelAdmin):
    pass
