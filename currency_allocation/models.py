from django.db import models
from django.urls import reverse
from extensions.models import DevelopedModel
from extensions.validators import validate_file_extension, validate_file_size
from extensions.utils import generate_random_number
from functools import partial
import random
import os


rand_with_8_digits = partial(generate_random_number, 8)
rand_with_9_digits = partial(generate_random_number, 9)


class TransactionType(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)

    class Meta:
        verbose_name = 'نوع معامله'
        verbose_name_plural = 'نوع معامله'

    def __str__(self):
        return self.title


class Undertaking(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)
    transaction_type = models.ForeignKey(
        TransactionType,
        verbose_name='نوع معامله',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'متعهد'
        verbose_name_plural = 'متعهد'

    def __str__(self):
        return self.title
        # return f'{self.transaction_type} -> {self.title}'


class FacilityLocation(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)
    undertaking = models.ForeignKey(
        Undertaking,
        verbose_name='متعهد',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'محل تسهیلات'
        verbose_name_plural = 'محل تسهیلات'

    def __str__(self):
        return self.title
        # return f'{self.undertaking} -> {self.title}'


class RepaymentDeadline(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)
    facility_location = models.ForeignKey(
        FacilityLocation,
        verbose_name='محل تسهیلات',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = verbose_name_plural = 'مهلت بازپرداخت'

    def __str__(self):
        return self.title
        # return f'{self.facility_location} -> {self.title}'


class SupplyCurrencyPlace(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)
    repayment_deadline = models.ForeignKey(
        RepaymentDeadline,
        verbose_name='مهلت بازپرداخت',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = verbose_name_plural = 'محل تامین ارز'

    def __str__(self):
        return self.title
        # return f'{self.repayment_deadline} -> {self.title}'


class CurrencyRate(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)
    supply_currency = models.ForeignKey(
        SupplyCurrencyPlace,
        verbose_name='محل تامین ارز',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = verbose_name_plural = 'نرخ ارز'

    def __str__(self):
        return self.title
        # return f'{self.supply_currency} -> {self.title}'


class RequestType(DevelopedModel):
    title = models.CharField('عنوان', max_length=50)
    currency_rate = models.ForeignKey(
        CurrencyRate,
        verbose_name='نرخ ارز',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = verbose_name_plural = 'نوع درخواست'

    def __str__(self):
        return self.title
        # return f'{self.currency_rate} -> {self.title}'


STATUS_CHOICES = {
    'c': '‌ابطال',
    'a': 'تخصیص یافته',
}


class CurrencyRequest(DevelopedModel):
    main_data = models.ForeignKey(
        "order_registration.MainData",
        verbose_name='پرونده ثبت سفارش',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name='کاربر',
        on_delete=models.CASCADE)
    request_amount_by_main_data_currency = models.FloatField(
        'مبلغ درخواست به ارز ثبت سفارش')
    currency = models.ForeignKey(
        "dashboard.Currency",
        verbose_name='ارز درخواست', on_delete=models.PROTECT
    )
    request_amount = models.FloatField('مبلغ در خواست')
    transaction_type = models.ForeignKey(
        TransactionType,
        verbose_name='نوع معامله',
        on_delete=models.PROTECT
    )
    undertaking = models.ForeignKey(
        Undertaking, verbose_name='متعهد', on_delete=models.PROTECT)
    facility_location = models.ForeignKey(
        FacilityLocation,
        verbose_name='محل تسهیلات',
        on_delete=models.PROTECT
    )

    repayment_deadline = models.ForeignKey(
        RepaymentDeadline,
        verbose_name='مهلت باز پرداخت',
        on_delete=models.PROTECT
    )
    supply_currency_place = models.ForeignKey(
        SupplyCurrencyPlace,
        verbose_name='محل تامین ارز',
        on_delete=models.PROTECT)
    currency_rate = models.ForeignKey(
        CurrencyRate,
        verbose_name='نرخ ارز',
        on_delete=models.PROTECT
    )
    request_type = models.ForeignKey(
        RequestType,
        verbose_name='نوع درخواست',
        on_delete=models.PROTECT
    )
    duration_per_month = models.PositiveIntegerField(
        'مدت به ماه (حداکثر ۰ ماه)',
    )
    expire_date = models.PositiveIntegerField(
        'مهلت انقضا(حداکثر تا ۴۵ روز)',
    )
    document = models.FileField(
        'مستندات پرونده',
        upload_to='currency_allocation/request/',
        max_length=500,
        validators=[validate_file_size, validate_file_extension],
        default=None,
        blank=True,
        null=True
    )
    row = models.PositiveSmallIntegerField('ردیف', default=1)
    status = models.CharField(
        'وضعیت',
        choices=STATUS_CHOICES,
        max_length=50,
        default='a'
    )
    parent_request = models.ForeignKey(
        "self",
        verbose_name='درخواست تخصیص',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name='children'
    )
    file_number = models.PositiveIntegerField(
        'شماره پرونده',
        default=rand_with_9_digits
    )
    request_update = models.BooleanField('درخواست تمدید دارد', default=False)

    class Meta:
        verbose_name = 'درخواست تخصیص ارز'
        verbose_name_plural = 'درخواست تخصیص ارز'
        ordering = ['-created_at', '-row']

    def __str__(self):
        return f'درخواست تخصیص ارز پرونده{self.main_data}'

    @property
    def document_name(self):
        base = os.path.basename(self.document.name)
        return os.path.splitext(base)[0]

    @property
    def document_extension(self):
        base = os.path.basename(self.document.name)
        return os.path.splitext(base)[1]

    def get_absolute_url(self):
        return reverse("currency_allocation:request_detail", kwargs={"pk": self.pk})
