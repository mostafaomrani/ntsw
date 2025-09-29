from django.db import models
from django.conf import settings
import random
from django.urls import reverse


def generate_random_number():
    return random.randint(100000000, 999999999)


class Inquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='کاربر', on_delete=models.CASCADE)
    inquiry_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    result = models.CharField(max_length=100)
    valid_until = models.DateField(null=True, blank=True)
    issued_at = models.DateField(null=True, blank=True)
    qualification_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class BusinessCard(models.Model):
    STATUS_CHOISES = {
        'FC': 'تایید نهایی'  # Final Confirmation
    }
    TYPE_CHOISES = {
        'p': 'حقیقی',
        'c': 'حقوقی'

    }
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='کاربر', on_delete=models.CASCADE)
    request_number = models.PositiveIntegerField(
        'شماره درخواست', default=generate_random_number)
    request_type = models.CharField(
        'نوع درخواست', max_length=50, default='صدور')
    created_at = models.DateTimeField('زمان ارسال', auto_now_add=True)
    status = models.CharField('وضعیت', max_length=5,
                              choices=STATUS_CHOISES, default='FC')
    card_type = models.CharField(
        'نوع', max_length=1, choices=TYPE_CHOISES, default='p')

    class Meta:
        verbose_name = "کارت بازرگانی"
        verbose_name_plural = "کارت‌های بازرگانی"

    def __str__(self):
        return f'درخواست صدور کارت بازرگانی با شماره {self.request_number} برای {self.user}'


class CompanyBase(models.Model):
    user = models.ForeignKey(
        "users.Customuser", verbose_name='کاربر', on_delete=models.CASCADE)
    OWNER_TYPE_CHOICES = {
        'g': 'دولتی',
        'p': 'خصوصی'
    }
    owner_type = models.CharField(
        'نوع مالکیت شرکت', max_length=1, choices=OWNER_TYPE_CHOICES)
    national_identifier = models.CharField('شناسه ملی شرکت', max_length=11)
    email = models.EmailField('پست الکترونیک شخصیت حقوقی', max_length=254)
    url = models.URLField('پایگاه اینترنتی شخصیت حقوقی',
                          max_length=200, default=None, blank=True, null=True)
    fax = models.CharField('نمابر شخصیت حقوقی', max_length=11)
    phone = models.CharField('تلفن ثابت شخصیت حقوقی', max_length=11)

    class Meta:
        verbose_name = verbose_name_plural = 'پایه حقوقی'

    def __str__(self):
        return self.national_identifier

    def get_absolute_url(self):
        return reverse("CompanyBase_detail", kwargs={"pk": self.pk})
