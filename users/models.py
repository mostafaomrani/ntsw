from django.contrib.auth.models import User  # یا مدل کاربر سفارشی شما
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

from datetime import timedelta, datetime
from decouple import config
import uuid

class Role(models.Model):
    code = models.CharField("کد نقش", max_length=10, unique=True)
    title = models.CharField("عنوان نقش", max_length=100)

    class Meta:
            db_table = "role"

    def __str__(self):
        return self.title
    

class CustomUser(AbstractUser):
    # ROLE_CHOICES = {
    #     'br': 'پایه حقیقی- فعال',  # base rolde
    #     'bt': 'پایه حقوقی- فعال',
    #     'bc': 'بازرگان حقیقی- فعال',  # business card
    #     'bl': 'بازرگان حقوقی- فعال',
    #     'it': 'تاجر - حقوقی - وارد کننده',  # internal trader
    # }

    # active_role = models.CharField(
    #     'نقش فعال', choices=ROLE_CHOICES, max_length=2, default='br'
    # )

    roles = models.ManyToManyField(
        Role,
        verbose_name="نقش‌ها",
        blank=True,
        related_name="users",
        db_table="customuser_roles" 
    )
    active_role = models.ForeignKey(
        Role,
        verbose_name="نقش فعال",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_users",
        db_column="active_role_id"  
    )

    
    first_name = models.CharField(
        'نام',
        max_length=150,
        blank=True,
        null=True,
        default=None)
    last_name = models.CharField(
        'نام‌خانوادگی',
        max_length=150,
        blank=True,
        null=True,
        default=None
    )
    national_code = models.CharField('کد ملی', max_length=10)
    birth_date = models.DateField('تاریخ تولد')
    mobile = models.CharField(
        'تلفن همراه',
        max_length=11,
        unique=True,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',  # فقط اعداد و دقیقاً ۱۱ رقم
                message="این فیلد باید دقیقاً شامل ۱۱ رقم باشد.",
            )
        ],
        help_text="این فیلد باید دقیقاً ۱۱ کاراکتر باشد.")
    is_mobile_verified = models.BooleanField(
        'تایید موبایل', default=False)
    phone = models.CharField('تلفن ثابت محل سکونت', max_length=11)
    postal_code = models.CharField('کد پستی محل سکونت', max_length=10)
    use_2fa = models.BooleanField(
        'مایل به استفاده از رمز دو عاملی هستم', default=False)
    avatar = models.ImageField(
        'تصویر پرسنلی', upload_to='uploads/users/avatar', max_length=100, blank=True, default=None)
    uuid = models.UUIDField('uuid کد', default=uuid.uuid4,
                            editable=False, unique=True)
    base = models.BooleanField('پایه حقیقی', default=True)
    has_business_card = models.BooleanField(
        'بازرگان حقیقی', default=False)
    has_internal_trader = models.BooleanField(
        'تاجر حقیقی', default=False)
    has_company_base = models.BooleanField(
        'پایه حقوقی',
        default=False
    )
    has_company_business_card = models.BooleanField(
        'بازرگان حقوقی', default=False)
    
    verification_response = models.TextField(
        'پیام درخواست نام و نام خانوادگی',
        default=None,
        blank=True,
        null=True
    )
    verification_response_result = models.BooleanField(
        'نتیجه درخواست نام و نام خانوادگی',
        default=False,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'

    def __str__(self):

        return self.get_full_name() if self.get_full_name() else self.username

    def clean(self):
        if len(self.mobile) != 11:
            raise ValidationError("طول این فیلد باید دقیقاً ۱۱ کاراکتر باشد.")


class TraderRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    action_name = models.CharField(max_length=100)
    activity_domain = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    not_show_for_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "trader_role"  # <-- اینجا نام جدول واقعی PostgreSQL
        managed = False  # Django این جدول را مدیریت نمی‌کند

    

class VerificationCode(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='کاربر', on_delete=models.CASCADE)
    uuid = models.UUIDField('uuid کد', default=uuid.uuid4,
                            editable=False, unique=True)
    created_at = models.DateTimeField('ایجاد شده در', auto_now_add=True)
    verification_code = models.PositiveIntegerField(
        'کد تایید',
        validators=[MinValueValidator(100000), MaxValueValidator(999999)]
    )
    response_status = models.PositiveSmallIntegerField('وضعیت ارسال')
    response_message = models.TextField('پیام وضعیت ارسال')

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'
        indexes = [
            models.Index(fields=['user', 'verification_code']),
        ]

    def __str__(self):
        return f'کد {self.verification_code} برای کاربر {self.user} ایجاد شد'

    @property
    def is_valid(self):
        time_turtling = config('SMS_TIME_TURTLING', cast=int, default=120)
        return self.created_at + timedelta(seconds=time_turtling) > timezone.now()
