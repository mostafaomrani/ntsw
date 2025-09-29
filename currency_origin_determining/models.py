from django.db import models
from extensions.models import DevelopedModel
from extensions.utils import generate_sata_code, generate_random_number
from functools import partial
from django.urls import reverse

rand_with_8_digit = partial(generate_random_number, 8)
rand_with_9_digit = partial(generate_random_number, 9)

STATUS_CHOICES = {
    'p': 'ترخیص شده',  # permitted
    'c': 'ابطال',  # canceled
    'r': 'اماده اظهار گمرکی'  # ready
}


class Banking(DevelopedModel):
    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name='کاربر',
        on_delete=models.CASCADE
    )
    main_data = models.ForeignKey(
        "order_registration.MainData",
        verbose_name='پرونده',
        on_delete=models.CASCADE
    )
    origin_country = models.ForeignKey(
        "dashboard.Country",
        verbose_name='کشور مبدا حمل',
        on_delete=models.PROTECT
    )
    entrance_edge = models.ForeignKey(
        "order_registration.EntranceEdge",
        verbose_name='مرز ورودی',
        on_delete=models.PROTECT
    )
    custom_destination = models.ForeignKey(
        "order_registration.Custom",
        verbose_name='گمرک مقصد',
        on_delete=models.PROTECT
    )
    fob_amount = models.FloatField('مبلغ فوب کالا', default=0)
    shipping_price = models.FloatField(
        'مبلغ حمل', default=None, blank=True, null=True)
    inspection_amount = models.FloatField(
        'مبلغ بازرسی',
        default=0
    )
    off = models.FloatField('تخفیف', default=0)
    other_cost = models.FloatField('سایر هزینه‌ها', default=0)
    total_price = models.FloatField('مبلغ کل')
    lading_bill_fob = models.FloatField('مبلغ فوب سند حمل')
    pay_number = models.PositiveIntegerField('شماره ابزار پرداخت')
    shipping_document = models.CharField(
        'سند حمل را انتخاب کنید', max_length=50)
    sata = models.CharField(
        'شماره ساتا',
        max_length=14,
        default=generate_sata_code
    )
    identifier = models.PositiveIntegerField(
        'کد یکتای منشا ارز',
        default=rand_with_8_digit
    )
    file_number = models.PositiveIntegerField(
        'شماره پرونده',
        default=rand_with_9_digit
    )
    status = models.CharField(
        'وضعیت',
        max_length=1,
        default="r",
        choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = verbose_name_plural = 'منشا ارز بانکی'
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return f'منشا ارز پرونده {self.main_data}'

    def get_absolute_url(self):
        return reverse("currency_origin_determining:banking_detail", kwargs={"pk": self.pk})


class LadingBill(DevelopedModel):
    banking = models.ForeignKey(
        Banking,
        verbose_name='منشا ارز بانکی',
        related_name='bilings',
        on_delete=models.CASCADE
    )
    identifier = models.CharField(
        'شماره بارنامه',
        max_length=50
    )
    date = models.DateField('تاریخ بارنامه')

    class Meta:
        verbose_name = verbose_name_plural = 'بارنامه'

    def __str__(self):
        return str(self.identifier)


class Ware(DevelopedModel):
    banking = models.ForeignKey(
        Banking,
        verbose_name='منشا ارز',
        on_delete=models.CASCADE,
        related_name='wares'
    )
    order_registraiton_ware = models.ForeignKey(
        "order_registration.Ware",
        verbose_name='کالاهای منشا ارز',
        on_delete=models.CASCADE
    )
    amount = models.FloatField('تعداد/مقدار')
    net_weight = models.FloatField('وزن خالص(کیلوگرم)')
    gross_weight = models.FloatField('وزن ناخالص(کیلوگرم)')
    packing_count = models.FloatField('تعداد بسته')

    class Meta:
        verbose_name = verbose_name_plural = 'کالاها'

    def __str__(self):
        return f'کالاهای منشا ارزی{self.banking}'


class WithoutCurrencyTransfer(DevelopedModel):
    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name='کاربر',
        on_delete=models.CASCADE)
    main_data = models.ForeignKey(
        "order_registration.MainData",
        verbose_name='پرونده',
        on_delete=models.CASCADE
    )
    origin_country = models.ForeignKey(
        "dashboard.Country",
        verbose_name='کشور مبدا حمل',
        on_delete=models.PROTECT
    )
    entrance_edge = models.ForeignKey(
        "order_registration.EntranceEdge",
        verbose_name='مرز ورودی',
        on_delete=models.PROTECT
    )
    custom_destination = models.ForeignKey(
        "order_registration.Custom",
        verbose_name='گمرک مقصد',
        on_delete=models.PROTECT
    )
    fob_amount = models.FloatField('مبلغ فوب کالا', default=0)
    shipping_price = models.FloatField(
        'مبلغ حمل', default=None, blank=True, null=True)
    inspection_amount = models.FloatField(
        'مبلغ بازرسی',
        default=0
    )
    off = models.FloatField('تخفیف', default=0)
    other_cost = models.FloatField('سایر هزینه‌ها', default=0)
    total_price = models.FloatField('مبلغ کل')
    lading_bill_fob = models.FloatField('مبلغ فوب سند حمل')
    pay_number = models.PositiveIntegerField('شماره ابزار پرداخت')
    shipping_document = models.CharField(
        'سند حمل را انتخاب کنید', max_length=50)
    sata = models.CharField(
        'شماره ساتا',
        max_length=14,
        default=generate_sata_code
    )
    identifier = models.PositiveIntegerField(
        'کد یکتای منشا ارز',
        default=rand_with_8_digit
    )
    file_number = models.PositiveIntegerField(
        'شماره پرونده',
        default=rand_with_9_digit
    )
    status = models.CharField(
        'وضعیت',
        max_length=1,
        default="r",
        choices=STATUS_CHOICES
    )

    class Meta:
        verbose_name = verbose_name_plural = 'منشا ارز بدون انتقال ارز'
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return f'منشا ارز پرونده {self.main_data}'

    def get_absolute_url(self):
        return reverse("currency_origin_determining:without_currency_transfer_detail", kwargs={"pk": self.pk})


class WithoutCurrencyTransferLadingBill(DevelopedModel):
    without_currency_transfer = models.ForeignKey(
        WithoutCurrencyTransfer,
        verbose_name='منشا ارز بدون انتقال ارز',
        on_delete=models.CASCADE,
        related_name='bilings'
    )
    tracking_code = models.CharField(
        'کد رهگیری بارنامه',
        max_length=50
    )
    identifier = models.CharField(
        'شماره بارنامه',
        max_length=50
    )
    date = models.DateField('تاریخ صدور بارنامه')

    class Meta:
        verbose_name = verbose_name_plural = 'بارنامه بدون انتقال ارز'

    def __str__(self):
        return f'بارنامه منشا ارز بدون انتقال ارز با شماره ثبت سفارش{self.without_currency_transfer}'


class WithoutCurrencyTransferWare(DevelopedModel):
    without_currency_transfer = models.ForeignKey(
        WithoutCurrencyTransfer,
        verbose_name='منشا ارز بدون انتقال ارز',
        on_delete=models.CASCADE,
        related_name='wares'
    )
    order_registraiton_ware = models.ForeignKey(
        "order_registration.Ware",
        verbose_name='کالاهای منشا ارز',
        on_delete=models.CASCADE
    )
    amount = models.FloatField('تعداد/مقدار')
    net_weight = models.FloatField('وزن خالص(کیلوگرم)')
    gross_weight = models.FloatField('وزن ناخالص(کیلوگرم)')
    packing_count = models.FloatField('تعداد بسته')

    class Meta:
        verbose_name = verbose_name_plural = 'کالاهای بدون انتقال ارز'

    def __str__(self):
        return f'کالاهای منشا ارزی بدون انتقال ارز {self.without_currency_transfer}'
