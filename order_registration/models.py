from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Sum
from extensions.utils import generate_random_number, six_month_after
from extensions.validators import validate_file_extension, validate_file_size
from functools import partial
from datetime import datetime, timedelta


rand_with_10_digits = partial(generate_random_number, 10)


class Incoterms(models.Model):
    title = models.CharField('عنوان', max_length=50)
    has_shipping_cost = models.BooleanField('هزینه حمل')

    class Meta:
        verbose_name = 'نوع قرارداد'
        verbose_name_plural = 'نوع قرارداد'

    def __str__(self):
        return self.title


class ShippingType(models.Model):
    title = models.CharField('عنوان', max_length=50)
    incoterms = models.ManyToManyField(
        Incoterms, related_name='incoterms', verbose_name='مرزهای ورودی')

    class Meta:
        verbose_name = "روش حمل"
        verbose_name_plural = "روش حمل"

    def __str__(self):
        return self.title


class EntranceEdge(models.Model):
    title = models.CharField('نام', max_length=50)
    shipping_type = models.ManyToManyField(
        ShippingType, verbose_name='روش حمل')

    class Meta:
        verbose_name = 'مرزهای ورودی'
        verbose_name_plural = 'مرزهای ورودی'

    def __str__(self):
        return self.title


class OrderRegistrationCase(models.Model):
    title = models.CharField('عنوان', max_length=50)
    order_by = models.PositiveSmallIntegerField(
        'مرتب سازی', default=0, blank=True)

    class Meta:
        verbose_name = 'حالت ثبت سفارش'
        verbose_name_plural = 'حالت ثبت سفارش'
        ordering = ['order_by']

    def __str__(self):
        return self.title


class Custom(models.Model):
    title = models.CharField('عنوان', max_length=100)

    class Meta:
        verbose_name = 'گمرک'
        verbose_name_plural = 'گمرک'

    def __str__(self):
        return self.title


class MainData(models.Model):
    PRODUCER_TYPE = {
        'i': 'صنعتی (بهین یاب)',  # industrial
        'g': 'صنفی',  # guild
        'm': 'معدنی',  # mineral
        'a': 'کشاورزی',  # agriculture
        'e': 'وزارت نیرو',  # energy
    }
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),  # draft
        ('n', 'جدید'),  # new
        ('ig', 'در حال استعلام'),  # inquiring,
        ('id', 'استعلام شده'),  # inquired
        ('w', 'منتظر مجوزها'),  # wating
        ('rr', 'آماده ثبت سفارش'),  # ready to register
        ('p', 'در حال ثبت سفارش'),  # Placing an order
        ('rp', 'آماده پرداخت کارمزد'),  # Ready to pay the fee
        ('r', 'ثبت سفارش'),  # registered
        ('c', 'ابطال شده'),  # canceled
    ]
    PERMISSION_CHOISES = {
        'f': 'کامل',  # full access
    }
    permission = models.CharField(
        'سطح دسترسی', choices=PERMISSION_CHOISES, max_length=1, default='f')
    identifier = models.PositiveIntegerField(
        'شماره پرونده', default=generate_random_number)
    proforma_invoice = models.CharField('شماره پیش فاکتور', max_length=50)
    beneficiary_country = models.ForeignKey(
        "dashboard.country", verbose_name='کشور ذینفع', on_delete=models.PROTECT)
    proforma_invoice_issue_date = models.DateField('تاریخ صدور پیش فاکتور')
    proforam_invoice_expire_date = models.DateField('تاریخ اعتبار پیش فاکتور')
    order_registration_case = models.ForeignKey(
        OrderRegistrationCase, verbose_name='حالت ثبت سفارش', on_delete=models.PROTECT)
    supplier_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('supplier_type', 'object_id')
    producer_type = models.CharField(
        'نوع واحدهای تولیدی', choices=PRODUCER_TYPE, max_length=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='کاربر', on_delete=models.CASCADE)
    status = models.CharField(
        'وضعیت پرونده', max_length=2, choices=STATUS_CHOICES, default='d')
    producer_type_data = models.CharField(
        'شناسه کسب و کار', max_length=50, default=None, blank=True, null=True)
    expire_date = models.DateField(
        'تاریخ اعتبار ثبت سفارش', default=six_month_after)
    document = models.FileField(
        'مستندات پروند', upload_to='order_registration/main_data', max_length=500, validators=[validate_file_size, validate_file_extension], default=None, blank=True, null=True)
    created_at = models.DateTimeField(
        'تاریخ ایجاد', auto_now_add=True)
    registrations_number = models.PositiveIntegerField(
        'شماره ثبت سفارش', default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'اطلاعات اصلی'
        verbose_name_plural = 'اطلاعات اصلی'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.identifier)

    def get_next_status(self, segment=1):
        """دریافت وضعیت بعدی"""
        status_keys = [choice[0] for choice in self.STATUS_CHOICES]
        try:
            current_index = status_keys.index(self.status)
            return status_keys[current_index + segment] if current_index + segment < len(status_keys) else None
        except ValueError:
            return None  # اگر مقدار نامعتبر باشد

    def get_next_status_from_current_status(self):
        if self.status == 'd':
            return 'n'
        if self.status == 'n':
            return 'id'
        if self.status == 'id':
            return 'rr'
        if self.status == 'rr':
            return 'rp'
        if self.status == 'rp':
            return 'r'
        return self.status

    @property
    def get_document_type(self):
        document = self.document
        if not document:
            return None
        filename = document.name.lower()
        return 'is_img' if filename.endswith(('.jpg', '.jpeg', '.png',)) else 'is_pdf'

    @property
    def ware_net_weight_sum(self):
        return sum([w.net_weight for w in self.ware_set.all()] or [0])

    @property
    def ware_gross_weight_sum(self):
        return sum([w.gross_weight for w in self.ware_set.all()] or [0])

    @property
    def ware_value_sum(self):
        total = self.ware_set.aggregate(
            total_value=Sum('fob_price'))['total_value']
        return total if total is not None else 0

    @property
    def total_price(self):
        """مبلغ کل پرونده:جمع مبلغ حمل و جمع فوب کالاها"""
        shipping_price = self.financial.shipping_price if self.financial.shipping_price else 0
        return self.ware_value_sum + shipping_price


class CustomsAndShipping(models.Model):
    SHIPPING_NATIONALITY = {
        'un': 'نامشخص',  # uncertain
        'ir': 'ایرانی',  # iranian
        'fo': 'خارجی',  # foreign
    }
    main_data = models.OneToOneField(
        MainData, verbose_name='داده‌های اصلی', on_delete=models.CASCADE, related_name='custom_and_shipping')
    incoterms = models.ForeignKey(
        Incoterms, verbose_name='نوع قرارداد', on_delete=models.PROTECT)
    shipping_all_at_once = models.BooleanField('حمل یکسره', default=False)
    shipping_period = models.BooleanField('حمل به دفعات', default=False)
    shipping_type = models.ManyToManyField(
        ShippingType, verbose_name='روش‌های حمل')
    entrance_edge = models.ManyToManyField(
        EntranceEdge, verbose_name='مرز ورودی')
    origin_country = models.ForeignKey(
        "dashboard.country", verbose_name='کشور مبدا حمل', on_delete=models.PROTECT)
    destination_custom = models.ManyToManyField(
        Custom, verbose_name='گمرک مقصد')

    loading_location = models.CharField(
        'محل بارگیری', max_length=50, default=None, blank=True)
    shipping_nationality = models.CharField(
        'ناوگان حمل و نقل', choices=SHIPPING_NATIONALITY, max_length=2)
    created_at = models.DateTimeField(
        'تاریخ ایجاد', auto_now_add=True)

    class Meta:
        verbose_name = 'گمرکی و حمل'
        verbose_name_plural = 'گمرکی و حمل'

    def __str__(self):
        return f'اطلاعات حمل و نقل پرونده با شماره{self.main_data.identifier}'

    @property
    def entrance_edges_str(self):
        """دریافت لیست مرزهای ورودی این پرونده به عنوان یک رشته جدا شده با ویرگول"""
        return ', '.join([edge.title for edge in self.entrance_edge.all()])

    @property
    def shipping_type_str(self):
        """دریافت لیست مرزهای ورودی این پرونده به عنوان یک رشته جدا شده با ویرگول"""
        return ', '.join([shipping.title for shipping in self.shipping_type.all()])

    @property
    def destination_custom_str(self):
        """دریافت لیست مرزهای ورودی این پرونده به عنوان یک رشته جدا شده با ویرگول"""
        return ', '.join([destination.title for destination in self.destination_custom.all()])

    @property
    def shipping_period_str(self):
        """تبدیل فیلد بولین به متن"""
        return 'مجاز' if self.shipping_period else 'غیر مجاز'

    @property
    def shipping_all_at_once_str(self):
        return 'مجاز' if self.shipping_all_at_once else 'غیر مجاز'


class Bank(models.Model):
    title = models.CharField('بانک', max_length=100, default=None, blank=True)

    class Meta:
        verbose_name = 'بانک'
        verbose_name_plural = 'بانک'

    def __str__(self):
        return self.title


class BankBranch(models.Model):
    title = models.CharField('عنوان', max_length=100)
    bank = models.ForeignKey(
        Bank, verbose_name='شعبه بانک', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'شعبه بانک'
        verbose_name_plural = 'شعبه بانک'

    def __str__(self):
        return self.title


CURRENCY_OPERATION_TYPE_CHOISES = {
    'b': 'بانکی',
    'nb': 'بدون انتقال ارز',
}


class CurrencySupply(models.Model):
    global CURRENCY_OPERATION_TYPE_CHOISES
    title = models.CharField('عنوان', max_length=300)
    currency_operation_type = models.CharField(
        'نوع عملیات ارزی',
        choices=CURRENCY_OPERATION_TYPE_CHOISES,
        max_length=2,
        default='b'
    )
    order = models.SmallIntegerField('مرتب سازی')

    class Meta:
        verbose_name = 'محل تامین ارز'
        verbose_name_plural = 'محل تامین ارز'
        ordering = ['order']

    def __str__(self):
        return self.title


class Financial(models.Model):
    global CURRENCY_OPERATION_TYPE_CHOISES
    PAYMENT_TYPE_CHOISES = {
        'ca': 'نقدی',
        'cr': 'اعتباری',
    }
    main_data = models.OneToOneField(
        MainData, verbose_name='داده‌های اصلی', on_delete=models.CASCADE)
    proforma_amount = models.DecimalField(
        'مبلغ کل پیش فاکتور', default=None, blank=True, null=True, max_digits=22, decimal_places=2)
    currency_type = models.ForeignKey(
        'dashboard.Currency', verbose_name='نوع ارز', on_delete=models.PROTECT)
    off_amount = models.DecimalField(
        'مبلغ تخفیف',
        default=None,
        blank=True,
        null=True,
        max_digits=22,
        decimal_places=2
    )
    currency_operation_type = models.CharField(
        'نوع عملیات ارزی', choices=CURRENCY_OPERATION_TYPE_CHOISES, max_length=2)
    bank = models.ForeignKey(Bank, verbose_name='بانک',
                             on_delete=models.CASCADE, default=None, blank=True, null=True)
    bank_branch = models.ForeignKey(
        BankBranch, verbose_name='شعبه', on_delete=models.CASCADE, default=None, blank=True, null=True)
    curency_supply = models.ManyToManyField(
        CurrencySupply, verbose_name='تامین ارز')
    shipping_price = models.DecimalField(
        'هزینه حمل', default=None, blank=True, null=True, max_digits=22, decimal_places=2)
    other_price = models.DecimalField(
        'سایر هزینه‌ها', default=None, blank=True, null=True, max_digits=22, decimal_places=2)
    payment_type = models.CharField(
        'نوع پرداخت', choices=PAYMENT_TYPE_CHOISES, max_length=2, default=None, blank=True)
    created_at = models.DateTimeField(
        'تاریخ ایجاد', auto_now_add=True)

    class Meta:
        verbose_name = 'مالی و بانکی'
        verbose_name_plural = 'مالی و بانکی'

    def __str__(self):
        return f'اطلاعات پرونده با شناسه{self.main_data}'

    @property
    def curency_supply_str(self):
        """دریافت لیست مرزهای ورودی این پرونده به عنوان یک رشته جدا شده با ویرگول"""
        return ', '.join([curency.title for curency in self.curency_supply.all()])


class ManufactureYear(models.Model):
    year = models.CharField('سال تولید', max_length=10)
    order_by = models.PositiveSmallIntegerField('مرتب سازی', default=1)

    class Meta:
        verbose_name = 'سال تولید'
        verbose_name_plural = 'سال تولید'
        ordering = ['order_by']

    def __str__(self):
        return self.year


class Packing(models.Model):
    title = models.CharField('عنوان', max_length=50)
    order_by = models.PositiveSmallIntegerField('مرتب سازی')

    class Meta:
        verbose_name = 'نوع بسته بندی'
        verbose_name_plural = 'نوع بسته بندی'
        ordering = ['order_by']

    def __str__(self):
        return self.title


class Ware(models.Model):
    # کالاهای پرونده
    REPRESENTATION_STATUS_CHOICES = {
        'ma': 'واردات به سرزمین اصلی',  # main area
        'su': 'واردات به مناطق آزاد و ويژه اقتصادی'  # sub area
    }
    UNIT_CHOISES = {
        'kg': 'کیلوگرم',
        'n': 'عدد',
        'm': 'متر',
        's': 'ست',
        'mm': 'مترمربع',
        'mmm': 'مترمکعب',
        'l': 'لیتر',
        'p': 'جفت',

    }
    STAUS_CHOICES = {
        'n': 'نو',
        'u': 'مستعمل',
        'r': 'بازسازی شده',
        'w': 'پسماند',
    }

    main_data = models.ForeignKey(
        MainData, verbose_name='اطلاعات اصلی', on_delete=models.CASCADE)
    virtual_code = models.BigIntegerField(
        'کد مجازی', default=rand_with_10_digits)
    hs_code = models.PositiveIntegerField('شماره تعرفه')
    representation_status = models.CharField(
        'وضعیت نمایندگی', choices=REPRESENTATION_STATUS_CHOICES, max_length=2)
    ware_identifier = models.PositiveIntegerField(
        'شناسه کالا', default=None, blank=True, null=True)
    organization_identifier = models.PositiveIntegerField(
        'شناسه سازمان', default=None, blank=True, null=True)
    persian_title = models.CharField('شرح تجاری فارسی', max_length=100)
    english_title = models.CharField('شرح تجاری انگلیسی', max_length=100)
    manufacture_year = models.ForeignKey(
        ManufactureYear, verbose_name='سال ساخت', on_delete=models.PROTECT)
    unit = models.CharField(
        'واحد اندازه گیری', max_length=3, choices=UNIT_CHOISES)
    fob_price = models.DecimalField(
        'مبلغ FOB', max_digits=22, decimal_places=2)
    off = models.PositiveIntegerField(
        'تخفیف',
        default=None,
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        'تعداد/مقدار', max_digits=22, decimal_places=2)
    net_weight = models.DecimalField(
        'وزن خالص(کیلوگرم)', max_digits=22, decimal_places=2)
    gross_weight = models.DecimalField(
        'وزن ناخالص(کیلوگرم)', max_digits=22, decimal_places=2)
    packing_type = models.ForeignKey(
        Packing,
        verbose_name='نوع بسته بندی',
        on_delete=models.PROTECT
    )
    status = models.CharField(
        'وضعیت کالا', choices=STAUS_CHOICES, max_length=1)
    made_country = models.ForeignKey(
        "dashboard.country", verbose_name='کشور تولید کننده', on_delete=models.PROTECT)
    technical_specifications = models.CharField(
        'مشخصات فنی',
        max_length=100,
        default=None,
        blank=True
    )
    standard = models.CharField(
        'استاندارد',
        max_length=100,
        default=None,
        blank=True
    )
    producer_name = models.CharField('نام تولید کننده', max_length=50)
    created_at = models.DateTimeField(
        'تاریخ ایجاد', auto_now_add=True)

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'

    def __str__(self):
        return f'کالای پرونده‌ی {self.main_data.id}'
# قیمت واحد

    @property
    def unit_price(self):
        unit_price = self.fob_price/self.amount
        return round(unit_price, 2)

    def clean(self):
        super().clean()  # اعتبارسنجی‌های پیش‌فرض جنگو را اجرا کنید
        # بررسی کنید که آیا هر دو فیلد خالی هستند
        if not self.technical_specifications and not self.standard:
            raise ValidationError({
                'technical_specifications': 'حداقل یکی از فیلدهای "مشخصات فنی" یا "استاندارد" باید پر شود.',
                'standard': 'حداقل یکی از فیلدهای "مشخصات فنی" یا "استاندارد" باید پر شود.',
            })
