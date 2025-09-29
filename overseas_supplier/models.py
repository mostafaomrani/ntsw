from django.db import models
from extensions.utils import generate_random_number
from functools import partial
from extensions.validators import validate_file_extension, validate_file_size

rand = partial(generate_random_number, 13)


class DocumentType(models.Model):
    name = models.CharField('نام', max_length=50)
    order_by = models.SmallIntegerField('مرتب سازی', default=0, blank=True)

    class Meta:
        verbose_name = 'نوع مدرک شناسایی'
        verbose_name_plural = 'نوع مدرک شناسایی'
        ordering = ['order_by', 'name']

    def __str__(self):
        return self.name


class CompanyOwnerType(models.Model):
    title = models.CharField('عنوان', max_length=50)
    order_by = models.SmallIntegerField('مرتب سازی', default=0, blank=True)

    class Meta:
        verbose_name = 'نوع مالکیت شرکت'
        verbose_name_plural = 'نوع مالکیت شرکت'
        ordering = ['order_by', 'title']

    def __str__(self):
        return self.title


class CompanyType(models.Model):
    title = models.CharField('نوع کمپانی', max_length=50)
    order = models.IntegerField('مرتب سازی', default=0, blank=True)

    class Meta:
        verbose_name = 'نوع شرکت'
        verbose_name_plural = 'نوع شرکت'

    def __str__(self):
        return self.title


class CompanySubject(models.Model):
    title = models.CharField('موضوع فعالیت', max_length=50)
    order_by = models.SmallIntegerField('مرتب سازی', default=0, blank=True)

    class Meta:
        verbose_name = 'موضوع فعالیت شرکت'
        verbose_name_plural = 'موضوع فعالیت شرکت'
        ordering = ['order_by']

    def __str__(self):
        return self.title


class supplier(models.Model):
    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name='کاربر مربوطه',
        on_delete=models.CASCADE
    )
    status = models.BooleanField("وضعیت", default=True)
    description = models.TextField('توضیحات')
    identifier = models.BigIntegerField(
        'شناسه فروشنده خارجی', default=rand)
    created_at = models.DateField('تاریخ ایجاد', auto_now_add=True)
    document = models.FileField(
        'انتخاب تصویر مدارک',
        upload_to='overseas_supplyer/supplier',
        max_length=500,
        validators=[validate_file_size, validate_file_extension],
        default=None,
        blank=True,
        null=True
    )
    document_flag = models.BooleanField('آپلود فایل')

    class Meta:
        abstract = True


class Person(supplier):
    GENDER_CHOISES = {
        'mail': 'مرد',
        'fmail': 'زن'
    }
    MARIED_CHOISES = {
        's': 'مجرد',
        'm': 'متاهل',
        'c': 'متارکه',
        'w': 'بیوه',
    }

    first_name = models.CharField('نام/ First Name', max_length=100)
    last_name = models.CharField('نام خانوادگی/ Last Name', max_length=100)
    father_name = models.CharField('نام پدر', max_length=100)
    mother_name = models.CharField(
        'نام مادر',
        max_length=100,
        default=None,
        blank=True
    )
    grandfather_name = models.CharField(
        'نام جد',
        max_length=100,
        blank=True,
        default=None
    )
    country = models.ForeignKey(
        "dashboard.Country", verbose_name='کشور محل تولد', on_delete=models.PROTECT)
    city = models.CharField('شهر محل تولد', max_length=50,
                            default=None,  blank=True)
    gender = models.CharField('جنسیت', choices=GENDER_CHOISES, max_length=5)
    birthday = models.DateField('تاریخ تولد')
    nationality = models.ForeignKey(
        "dashboard.Country", verbose_name='ملیت', related_name='natinality_country', on_delete=models.PROTECT)
    maried = models.CharField(
        'وضعیت تاهل', max_length=50, choices=MARIED_CHOISES)  # tod: add choises
    personal_image = models.ImageField(
        'تصویر پرسنلی',
        upload_to='overseas_supplier/',
        max_length=1000,
        default=None,
        blank=True
    )
    document_type = models.ForeignKey(
        DocumentType,
        verbose_name='نوع مدرک شناسایی',
        on_delete=models.CASCADE
    )
    document_number = models.CharField('شماره مدرک شناسایی', max_length=100)
    issue_date = models.DateField('تاریخ صدور')
    expire_date = models.DateField('تاریخ انقضا')

    class Meta:
        verbose_name = 'شخص حقیقی'
        verbose_name_plural = 'شخص حقیقی'
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name


class Company(supplier):

    name = models.CharField('نام فارسی شرکت خارجی', max_length=100)
    en_name = models.CharField('نام لاتین شرکت خارجی', max_length=100)
    register_number = models.PositiveIntegerField('شماره ثبت')
    company_type = models.ForeignKey(
        CompanyType, verbose_name='نوع شرکت', on_delete=models.PROTECT)
    registered_country = models.ForeignKey(
        "dashboard.country", verbose_name='کشور محل ثبت', on_delete=models.PROTECT)
    registered_date = models.DateField('تاریخ ثبت')
    registered_from = models.ForeignKey(
        "dashboard.country", verbose_name='تابعیت ثبتی شرکت', related_name='registered_from', on_delete=models.PROTECT)
    owner_type = models.ForeignKey(
        CompanyOwnerType, verbose_name='نوع مالکیت', on_delete=models.PROTECT, default=None, blank=True)
    subject = models.ForeignKey(
        CompanySubject, verbose_name='موضوع فعالیت شرکت', on_delete=models.PROTECT)
    country = models.ForeignKey(
        "dashboard.country", verbose_name='کشور', related_name='country', on_delete=models.PROTECT)
    city = models.CharField('شهر', max_length=50)
    address = models.TextField('آدرس')
    postal_code = models.PositiveIntegerField(
        'کد پستی', default=None, blank=True, null=True)
    phone = models.CharField('تلفن', max_length=20)

    class Meta:
        verbose_name = 'شرکت'
        verbose_name_plural = 'شرکت‌'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
