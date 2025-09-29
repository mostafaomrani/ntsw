import os
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size  # اندازه فایل به بایت
    if filesize > 400 * 1024:  # ۴۰۰ کیلوبایت = 400 * 1024 بایت
        raise ValidationError("حجم فایل نباید بیش از ۴۰۰ کیلوبایت باشد.")


def validate_file_extension(value):
    # پسوند فایل
    ext = os.path.splitext(value.name)[1]  # مانند '.jpg' یا '.png'
    allowed_extensions = ['.jpg', '.jpeg',
                          '.pdf', '.png', '.docx', '.doc', '.txt']

    if ext.lower() not in allowed_extensions:
        raise ValidationError(f"فقط فایل‌های با پسوند {', '.join(allowed_extensions)} مجاز هستند.")
