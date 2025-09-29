import random
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import requests
import json
from decouple import config
import logging

logger = logging.getLogger('myproject.custom')


def generate_random_number(len=9):
    if len < 1:
        raise ValueError('طول عدد باید بزرگتر از صفر باشد')
    return random.randint(10**(len-1), 10**len - 1)


def six_month_after():
    return datetime.now() + timedelta(days=6*30)


def convert_currncy(amount, origin=0, destination=0):
    return amount


def send_sms(receptor, token):
    url = config('KAVENEGAR_SMS_URL')
    url = url.format(receptor=receptor, token=token)
    if config('IS_DEVELOPMENT_ENVIRONMENT', cast=bool):
        print(receptor, token)
        return {'status': 200, 'message': 'کد تایید چاپ شد'}
    try:
        response = requests.get(url)
    except Exception as e:
        return {
            'status': 500,
            'message': e
        }
    kavenegar_staus_code = [
        418,  # اعتبار حساب شما کافی نیست
        422,  # داده ها به دلیل وجود کاراکتر نامناسب قابل پردازش نیست
        424,  # الگوی مورد نظر پیدا نشد ، زمانی که نام الگو نادرست باشد یا طرح آن هنوز تائید نشده باشد رخ می‌دهد
        426,  # استفاده از این متد نیازمند سرویس پیشرفته می‌باشد
        428,  # ارسال کد از طریق تماس تلفنی امکان پذیر نیست، درصورتی که توکن فقط حاوی عدد نباشد این خطا رخ می‌دهد
        431,  # ساختار کد صحیح نمی‌باشد ، اگر توکن حاوی خط جدید،فاصله، UnderLine یا جداکننده باشد این خطا رخ می‌دهد
        432,  # پارامتر کد در متن پیام پیدا نشد ، اگر در هنگام تعریف الگو پارامتر token % را تعریف نکرده باشید این خطا رخ می‌دهد
        200,  # تایید شده
    ]
    response_dict = json.loads(response.text)
    if response.status_code in kavenegar_staus_code:
        return response_dict['return']
    return {
        'status': response.status_code,
        'message': response_dict.get('message', 'خطای نا مشخص در ارسال کد تایید')
    }


def generate_sata_code():
    prefix = '14030000'
    sufix = str(generate_random_number(6))
    return prefix + sufix


def zibal_national_identity_inquiry(national_code: str, birth_date: str) -> dict:
    """
    تابع برای استعلام هویت ملی از طریق API زیبال

    :param national_code: کد ملی (به عنوان رشته)
    :param birth_date: تاریخ تولد (به فرمت YYYY/MM/DD)
    :param bearer_token: توکن احراز هویت (Bearer Token)
    :return: پاسخ سرور به صورت دیکشنری یا None در صورت خطا
    """
    bearer_token = config('ZIBAL_BEARER_TOKEN')
    url = "https://api.zibal.ir/v1/facility/nationalIdentityInquiry/"

    payload = {
        "nationalCode": national_code,
        "birthDate": birth_date
    }
    print(payload)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        # ارسال درخواست POST
        response = requests.post(url, json=payload, headers=headers)
        server_response = response.json()
        result = server_response.get('result')
        if response.status_code == 200 and result == 1:
            data = server_response.get('data')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            return True, first_name, last_name
        else:
            msg = server_response.get('message')
            logger.error(msg)
            return False, msg

    except requests.exceptions.RequestException as e:
        logger.error(f"خطا در ارتباط با سرور زیبال: {e}")
        return False, 'error in zibal connection'
