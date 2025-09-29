from django import forms
from django.forms import inlineformset_factory
from currency_allocation.models import CurrencyRequest
from order_registration.models import MainData
from .models import (Banking,
                     LadingBill,
                     Ware,
                     WithoutCurrencyTransfer,
                     WithoutCurrencyTransferLadingBill,
                     WithoutCurrencyTransferWare,
                     )


class SelectMainDataForm(forms.ModelForm):

    class Meta:
        model = CurrencyRequest
        fields = ("main_data",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SelectMainDataForm, self).__init__(*args, **kwargs)
        self.fields['main_data'].queryset = MainData.objects.filter(
            user=user,
            status='r',
            financial__currency_operation_type='b'
        )
        self.fields['main_data'].label = 'کد ثبت سفارش'


class BankingForm(forms.ModelForm):
    class Meta:
        model = Banking
        fields = (
            'shipping_document',
            'origin_country',
            'entrance_edge',
            'custom_destination',
            'fob_amount',
            'shipping_price',
            'inspection_amount',
            'off',
            'other_cost',
            'total_price',
            'pay_number',
            'lading_bill_fob',
        )

    def __init__(self, *args, **kwargs):
        main_data = kwargs.pop('main_data')
        super().__init__(*args, **kwargs)
        other_cost = 0
        if main_data.financial.shipping_price:
            self.fields['shipping_price'].initial = main_data.financial.shipping_price
        if main_data.financial.other_price:
            other_cost = main_data.financial.other_price
        if main_data.financial.off_amount:
            other_cost = main_data.financial.off_amount

        self.fields['other_cost'].initial = other_cost
        self.fields["shipping_price"].widget.attrs["readonly"] = True
        self.fields["pay_number"].widget.attrs["readonly"] = True
        self.fields["fob_amount"].widget.attrs["readonly"] = True
        self.fields["inspection_amount"].widget.attrs["readonly"] = True
        self.fields["off"].widget.attrs["readonly"] = True
        self.fields["other_cost"].widget.attrs["readonly"] = True
        self.fields["total_price"].widget.attrs["readonly"] = True
        self.fields["lading_bill_fob"].widget.attrs["readonly"] = True
        self.fields["total_price"].initial = main_data.total_price + other_cost


class LadingBillForm(forms.ModelForm):

    class Meta:
        model = LadingBill
        fields = (
            'identifier',
            'date',)


class WareForm(forms.ModelForm):
    class Meta:
        model = Ware
        fields = (
            'order_registraiton_ware',
            'amount',
            'net_weight',
            'gross_weight',
            'packing_count',
        )


LadingBillingFormSet = inlineformset_factory(
    Banking,
    LadingBill,
    form=LadingBillForm,
    extra=0,
    can_delete=True
)


class SelectMainDataFormForWithoutCurrencyTransfer(forms.ModelForm):

    class Meta:
        model = CurrencyRequest
        fields = ("main_data",)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(
            SelectMainDataFormForWithoutCurrencyTransfer,
            self
        ).__init__(*args, **kwargs)
        self.fields['main_data'].queryset = MainData.objects.filter(
            user=user,
            status='r',
            financial__currency_operation_type='nb'
        )
        self.fields['main_data'].label = 'کد ثبت سفارش'


class WithoutCurrencyTransferForm(forms.ModelForm):
    class Meta:
        model = WithoutCurrencyTransfer
        fields = (
            'shipping_document',
            'origin_country',
            'entrance_edge',
            'custom_destination',
            'fob_amount',
            'shipping_price',
            'inspection_amount',
            'off',
            'other_cost',
            'total_price',
            'pay_number',
            'lading_bill_fob',
        )

    def __init__(self, *args, **kwargs):
        main_data = kwargs.pop('main_data')
        super().__init__(*args, **kwargs)
        if main_data.financial.shipping_price:
            self.fields['shipping_price'].initial = main_data.financial.shipping_price
        if main_data.financial.other_price:
            self.fields['other_cost'].initial = main_data.financial.other_price
        if main_data.financial.off_amount:
            self.fields['other_cost'].initial = main_data.financial.off_amount
        main_data_wares = main_data.ware_set.all()
        lading_bill_fob = 0
        for w in main_data_wares:
            lading_bill_fob = + w.fob_price

        self.fields["shipping_price"].widget.attrs["readonly"] = True
        self.fields["pay_number"].widget.attrs["readonly"] = True
        self.fields["fob_amount"].widget.attrs["readonly"] = True
        self.fields["inspection_amount"].widget.attrs["readonly"] = True
        self.fields["off"].widget.attrs["readonly"] = True
        self.fields["other_cost"].widget.attrs["readonly"] = True
        self.fields["total_price"].widget.attrs["readonly"] = True
        self.fields["lading_bill_fob"].widget.attrs["readonly"] = True
        self.fields["total_price"].initial = main_data.total_price
        self.fields["lading_bill_fob"].initial = lading_bill_fob


class WithoutCurrencyTransferLadingBillForm(forms.ModelForm):

    class Meta:
        model = WithoutCurrencyTransferLadingBill
        fields = (
            'tracking_code',
            'identifier',
            'date',)


class WithoutCurrencyTransferWareForm(forms.ModelForm):
    class Meta:
        model = WithoutCurrencyTransferWare
        fields = (
            'order_registraiton_ware',
            'amount',
            'net_weight',
            'gross_weight',
            'packing_count',
        )


WithoutCurrencyTransferLadingBillingFormSet = inlineformset_factory(
    WithoutCurrencyTransfer,
    WithoutCurrencyTransferLadingBill,
    form=WithoutCurrencyTransferLadingBillForm,
    extra=0,
    can_delete=True
)
