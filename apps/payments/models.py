from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='کاربر',
        related_name='payments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ref_id = models.PositiveBigIntegerField(default=0)
    gateway = models.CharField(max_length=50)
    amount = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField('شناسه', max_length=100)
    meta = models.JSONField('اطلاعات اضافی پرداخت', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(
        "order_registration.MainData",
        verbose_name='اطلاعات خرید',
        on_delete=models.CASCADE,
        related_name='payments',
    )

    def __str__(self):
        return f"{self.gateway} - {self.amount}"
