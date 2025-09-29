from django import forms
from django.db.models import F
from order_registration.models import MainData
from .models import (
    CurrencyRequest,
    Undertaking,
    FacilityLocation,
    RepaymentDeadline,
    SupplyCurrencyPlace,
    CurrencyRate,
    RequestType
)


class SelectMainDataForm(forms.ModelForm):

    class Meta:
        model = CurrencyRequest
        fields = ("main_data",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SelectMainDataForm, self).__init__(*args, **kwargs)
        self.fields['main_data'].label = 'شماره ثبت سفارش'
        self.fields['main_data'].queryset = MainData.objects.filter(
            user=user,
            status='r'
        )


class RequestForm(forms.ModelForm):

    class Meta:
        model = CurrencyRequest
        fields = (
            'request_amount_by_main_data_currency',
            'currency',
            'request_amount',
            'transaction_type',
            'undertaking',
            'facility_location',
            'repayment_deadline',
            'supply_currency_place',
            'currency_rate',
            'request_type',
            'duration_per_month',
            'expire_date',
            'document',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["request_amount"].widget.attrs["readonly"] = True
        if self.data:
            self.fields['undertaking'].queryset = Undertaking.objects.all()
            self.fields['facility_location'].queryset = FacilityLocation.objects.all()
            self.fields['repayment_deadline'].queryset = RepaymentDeadline.objects.all(
            )
            self.fields['supply_currency_place'].queryset = SupplyCurrencyPlace.objects.all(
            )
            self.fields['currency_rate'].queryset = CurrencyRate.objects.all()
            self.fields['request_type'].queryset = RequestType.objects.all()
        else:
            # اگر فرم در حال نمایش اولیه است، queryset را خالی نگه دارید
            self.fields['undertaking'].queryset = Undertaking.objects.none()
            self.fields['facility_location'].queryset = FacilityLocation.objects.none(
            )
            self.fields['repayment_deadline'].queryset = RepaymentDeadline.objects.none(
            )
            self.fields['supply_currency_place'].queryset = SupplyCurrencyPlace.objects.none(
            )
            self.fields['currency_rate'].queryset = CurrencyRate.objects.none()
            self.fields['request_type'].queryset = RequestType.objects.none()


class CurrencyRequestUpdateForm(forms.ModelForm):

    class Meta:
        model = CurrencyRequest
        fields = (
            'request_amount_by_main_data_currency',
            'currency',
            'request_amount',
            'transaction_type',
            'undertaking',
            'facility_location',
            'repayment_deadline',
            'supply_currency_place',
            'currency_rate',
            'request_type',
            'duration_per_month',
            'expire_date',
            'document',
            'request_update',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["request_amount"].widget.attrs["readonly"] = True
        if self.data:
            self.fields['undertaking'].queryset = Undertaking.objects.all()
            self.fields['facility_location'].queryset = FacilityLocation.objects.all()
            self.fields['repayment_deadline'].queryset = RepaymentDeadline.objects.all(
            )
            self.fields['supply_currency_place'].queryset = SupplyCurrencyPlace.objects.all(
            )
            self.fields['currency_rate'].queryset = CurrencyRate.objects.all()
            self.fields['request_type'].queryset = RequestType.objects.all()
        else:
            q = Undertaking.objects.filter(
                transaction_type=self.instance.transaction_type)
            self.fields['undertaking'].queryset = q
            self.fields['facility_location'].queryset = FacilityLocation.objects.filter(
                undertaking=self.instance.undertaking
            )
            self.fields['repayment_deadline'].queryset = RepaymentDeadline.objects.filter(
                facility_location=self.instance.facility_location
            )
            self.fields['supply_currency_place'].queryset = SupplyCurrencyPlace.objects.filter(
                repayment_deadline=self.instance.repayment_deadline
            )
            self.fields['currency_rate'].queryset = CurrencyRate.objects.filter(
                supply_currency=self.instance.supply_currency_place
            )
            self.fields['request_type'].queryset = RequestType.objects.filter(
                currency_rate=self.instance.currency_rate
            )


class CurrencyRequestDecompositionForm(forms.Form):
    current_currency_request = forms.FloatField(
        label='مبلغ درخواست فعلی',
        required=True
    )
    new_currency_request = forms.FloatField(
        label='مبلغ درخواست جدید',
        required=True
    )
