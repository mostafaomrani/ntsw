from django.db import models
from django.conf import settings 
from anbar.models import Anbar
from shenase.models import Shenase



class Foreintrade(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class DocumentTradeOperation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'باطل شده'),
    ]

    document_number = models.CharField(max_length=50, verbose_name="شماره سند")
    document_date = models.DateField(verbose_name="تاریخ سند")
    register_date = models.DateField(verbose_name="تاریخ ثبت")
    document_type = models.CharField(max_length=100, verbose_name="نوع سند")
    seller = models.CharField(max_length=255, verbose_name="فروشنده")
    origin = models.CharField(max_length=100, verbose_name="مبدأ")
    destination = models.CharField(max_length=100, verbose_name="مقصد")
    bill_number = models.CharField(max_length=50, verbose_name="شماره بارنامه")
    description = models.TextField(blank=True, verbose_name="شرح سند")
    
    # فیلد وضعیت با choices
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت"
    )

    anbar = models.ForeignKey(
        "anbar.Anbar",
        on_delete=models.CASCADE,
        verbose_name="انبار"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    class Meta:
        db_table = "domestic_trade_operations"
        verbose_name = "سند"
        verbose_name_plural = "اسناد"

    def __str__(self):
        return f"{self.document_number} - {self.seller}"




class AnbarItem(models.Model):
    UNIT_CHOICES = [
        ("ton", "تن"),
        ("kg", "کیلوگرم"),
        ("liter", "لیتر"),
        ("sheet", "ورق"),
        ("cubic_meter", "مترمکعب"),
        ("pcs", "عدد"),
        ("meter", "متر"),
        ("square_meter", "متر مربع"),
    ]

    anbar = models.ForeignKey(Anbar, on_delete=models.CASCADE, verbose_name="انبار")
    shenase = models.ForeignKey(Shenase, on_delete=models.CASCADE, verbose_name="شناسه کالا")
    description = models.CharField(max_length=255, verbose_name="شرح کالا")
    available_quantity = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="مقدار قابل استفاده")
    actual_quantity = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="مقدار واقعی")
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, verbose_name="واحد اندازه‌گیری")

    class Meta:
        db_table = "anbar_item"
        verbose_name = "کالای انبار"
        verbose_name_plural = "کالاهای انبار"

    def __str__(self):
        return f"{self.description} - {self.anbar.name}"