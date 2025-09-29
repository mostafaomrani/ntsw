from django import template
from persiantools.jdatetime import JalaliDate

register = template.Library()


@register.filter
def to_jalali(value):
    """
    Converts a Gregorian date to Jalali.
    Expects a datetime.date or datetime.datetime object.
    """
    if not value:
        return ""
    try:
        # تبدیل تاریخ میلادی به شمسی
        jalali_date = JalaliDate(value)
        return jalali_date.strftime("%Y/%m/%d")  # فرمت دلخواه
    except Exception as e:
        return str(e)  # برای نمایش خطا در صورت وجود
