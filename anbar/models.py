from django.db import models
from django.conf import settings


class Anbar(models.Model):

    STATUS_CHOICES = [
        ("active", "فعال"),
        ("inactive", "غیرفعال"),
    ]


    name = models.CharField(max_length=255, verbose_name="نام انبار")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی", blank=True, null=True)
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)
    organization = models.CharField(max_length=255, verbose_name="بهره بردار/سازمان متولی", blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="بهره بردار"
    )
    
    status = models.CharField(
        max_length=50,
        verbose_name="وضعیت",
        choices=STATUS_CHOICES,
        default="active"
    )

    class Meta:
        db_table = "anbar"
        verbose_name = "انبار"
        verbose_name_plural = "انبارها"

    def __str__(self):
        return self.name