from django.contrib import admin
from .models import (
    CurrencyRequest,
    TransactionType,
    Undertaking,
    FacilityLocation,
    RepaymentDeadline,
    SupplyCurrencyPlace,
    CurrencyRate,
    RequestType,
    CurrencyRequest,
)


@admin.action(description='Set user based on main_data')
def set_user_based_on_main_data(modeladmin, request, queryset):
    for currency_request in queryset:
        if currency_request.main_data and currency_request.main_data.user:
            currency_request.user = currency_request.main_data.user
            currency_request.save()


@admin.register(CurrencyRequest)
class RequestAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('id', 'main_data', 'user')
    actions = [set_user_based_on_main_data]  # اضافه کردن اکشن سفارشی


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Undertaking)
class UndertakingAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_type',
        'title',
    ]


@admin.register(FacilityLocation)
class FacilityLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(RepaymentDeadline)
class RepaymentDeadlineAdmin(admin.ModelAdmin):
    pass


@admin.register(SupplyCurrencyPlace)
class SupplyCurrencyPlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    pass


@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    pass
