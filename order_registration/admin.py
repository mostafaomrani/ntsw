from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from .models import (
    OrderRegistrationCase,
    Custom,
    EntranceEdge,
    ShippingType,
    Incoterms,
    MainData,
    CustomsAndShipping,
    Bank,
    BankBranch, CurrencySupply,
    Financial,
    ManufactureYear,
    Packing,
    Ware,
    CurrencySupply,

)


@admin.register(OrderRegistrationCase)
class OrderRegistrationCaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Custom)
class CustomAdming(ImportExportModelAdmin):
    pass


@admin.register(EntranceEdge)
class EntranceEdgeAdming(ImportExportModelAdmin):
    list_display = [
        'title',
    ]
    search_fields = [
        'title',
    ]
    list_filter = [
        'shipping_type'
    ]


@admin.register(ShippingType)
class ShippingTypeAdming(admin.ModelAdmin):
    pass


@admin.register(Incoterms)
class IncotermsAdming(admin.ModelAdmin):
    pass


@admin.register(MainData)
class MainDataAdming(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'registrations_number',
        'identifier',
        'created_at'
    ]
    list_filter = [
        'user',
        'registrations_number',
        'identifier',
        'created_at'
    ]
    search_fields = [
        'pk',
        'user',
        'registrations_number',
        'identifier',
    ]


@admin.register(CustomsAndShipping)
class CustomsAndShippingAdming(admin.ModelAdmin):
    list_display = [
        'pk',
        'main_data',
        'created_at'

    ]
    list_filter = [
        'main_data',
        'created_at'
    ]
    search_fields = [
        'pk',
        'main_data',
        'created_at'

    ]


@admin.register(Bank)
class BankAdming(ImportExportModelAdmin):
    pass


@admin.register(BankBranch)
class BankBranch(ImportExportModelAdmin):
    list_display = (
        'id',
        'title',
        'bank',
    )


@admin.register(CurrencySupply)
class CurrencySupplyAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'id'
    ]


@admin.register(Financial)
class FinancialAdming(admin.ModelAdmin):
    list_display = [
        'pk',
        'main_data',
        'created_at'
    ]
    list_filter = [
        'main_data',
        'created_at'

    ]
    search_fields = [
        'pk',
        'main_data',
        'created_at'

    ]


@admin.register(ManufactureYear)
class ManufactureYearAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'year'
    )


@admin.register(Packing)
class PackingAdming(admin.ModelAdmin):
    pass


@admin.register(Ware)
class WareAdming(admin.ModelAdmin):
    list_display = [
        'pk',
        'main_data',
        'created_at'
    ]
    list_filter = [
        'main_data',
        'created_at'
    ]
    search_fields = [
        'pk',
        'main_data',
        'created_at'

    ]
