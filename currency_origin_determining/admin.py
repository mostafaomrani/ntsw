from django.contrib import admin
from .models import Banking, Ware, LadingBill, WithoutCurrencyTransfer, WithoutCurrencyTransferLadingBill, WithoutCurrencyTransferWare


@admin.register(Banking)
class BankingAdmin(admin.ModelAdmin):
    pass


@admin.register(Ware)
class WareAdmin(admin.ModelAdmin):
    pass


@admin.register(LadingBill)
class LadingBillAdmin(admin.ModelAdmin):
    pass


@admin.register(WithoutCurrencyTransfer)
class WithoutCurrencyTransferAdmin(admin.ModelAdmin):
    pass


@admin.register(WithoutCurrencyTransferLadingBill)
class WithoutCurrencyTransferLadingBillAdmin(admin.ModelAdmin):
    pass


@admin.register(WithoutCurrencyTransferWare)
class WithoutCurrencyTransferWareAdmin(admin.ModelAdmin):
    pass
