from django.contrib.contenttypes.models import ContentType
from django import forms
from .models import MainData, CustomsAndShipping, Financial, Ware
from overseas_supplier.models import Person, Company
from django.core.exceptions import ValidationError


class MainDataForm(forms.ModelForm):
    supplier = forms.ChoiceField(
        choices=[
            ('', 'انتخاب کنید'),
            ('person', 'شخص حقیقی'),
            ('company', 'شخص حقوقی'),
        ],
        label="نوع فروشنده خارجی"
    )
    producer_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=MainData.PRODUCER_TYPE
    )
    related_object_id = forms.IntegerField(label='شناسه فروشنده خارجی')

    class Meta:
        model = MainData
        fields = (
            "proforma_invoice",
            'beneficiary_country',
            'proforma_invoice_issue_date',
            'proforam_invoice_expire_date',
            'order_registration_case',
            'producer_type',
            'related_object_id',
            'supplier',
            'producer_type_data',
        )


class CustomsAndShippingForm(forms.ModelForm):

    class Meta:
        model = CustomsAndShipping
        fields = (
            'incoterms',
            'shipping_all_at_once',
            'shipping_period',
            'shipping_type',
            'entrance_edge',
            'destination_custom',
            'loading_location',
            'shipping_nationality',
            'origin_country',
        )


class FinancialForm(forms.ModelForm):

    class Meta:
        model = Financial
        fields = (
            'proforma_amount',
            'currency_type',
            'off_amount',
            'currency_operation_type',
            'bank_branch',
            'curency_supply',
            'shipping_price',
            'other_price',
            'payment_type',
            'bank',
        )

    def __init__(self, *args, **kwargs):
        has_shipping_cost = kwargs.pop('has_shipping_cost', None)
        super().__init__(*args, **kwargs)
        if not has_shipping_cost:
            self.fields.pop('shipping_price')


class WareForm(forms.ModelForm):

    class Meta:
        model = Ware
        fields = ('hs_code',
                  'representation_status',
                  'ware_identifier',
                  'organization_identifier',
                  'persian_title',
                  'english_title',
                  'manufacture_year',
                  'unit',
                  'fob_price',
                  'off',
                  'amount',
                  'net_weight',
                  'gross_weight',
                  'packing_type',
                  'status',
                  'made_country',
                  'technical_specifications',
                  'standard',
                  'producer_name',
                  )

    def clean(self):
        cleaned_data = super().clean()
        technical_specifications = cleaned_data.get('technical_specifications')
        standard = cleaned_data.get('standard')

        # بررسی کنید که آیا هر دو فیلد خالی هستند
        if not technical_specifications and not standard:
            raise ValidationError({
                'technical_specifications': 'حداقل یکی از فیلدهای "مشخصات فنی" یا "استاندارد" باید پر شود.',
                'standard': 'حداقل یکی از فیلدهای "مشخصات فنی" یا "استاندارد" باید پر شود.',
            })

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ware_identifier"].widget.attrs["readonly"] = True
        self.fields["organization_identifier"].widget.attrs["readonly"] = True


class MainDataUploadDocumentForm(forms.ModelForm):

    class Meta:
        model = MainData
        fields = (
            "document",
        )
