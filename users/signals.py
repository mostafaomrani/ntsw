from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from extensions.utils import zibal_national_identity_inquiry
from persiantools.jdatetime import JalaliDate


User = get_user_model()


@receiver(post_save, sender=User)
def verify_user_national_identity(sender, instance, created, **kwargs):
    if created and instance.national_code and instance.birth_date:
        # فراخوانی API زیبال
        birth_date = JalaliDate.to_jalali(
            instance.birth_date
        ).strftime("%Y/%m/%d")

        result, *data = zibal_national_identity_inquiry(
            national_code=instance.national_code,
            birth_date=birth_date,
        )
        instance.is_verified = result

        if result:
            # استخراج نام و نام خانوادگی از پاسخ API
            first_name = data[0]
            last_name = data[1]
            # ذخیره اطلاعات در مدل کاربر
            instance.first_name = first_name
            instance.last_name = last_name
            instance.is_verified = result
            instance.verification_response = 'موفق'
            update_fields = [
                'first_name',
                'last_name',
                'is_verified',
                'verification_response',
            ]
        else:
            instance.verification_response = data[0]
            update_fields = [
                'is_verified',
                'verification_response',
            ]

            # ذخیره تغییرات (بدون فراخوانی سیگنال مجدد)
        instance.save()
