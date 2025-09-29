class PaymentError(Exception):
    """کلاس پایه برای تمام خطاهای مربوط به پرداخت"""
    default_message = "خطای عمومی پرداخت رخ داده است"

    def __init__(self, message=None, *args, **kwargs):
        self.message = message or self.default_message
        self.extra_data = kwargs
        super().__init__(self.message, *args)


class PaymentGatewayError(PaymentError):
    """خطای پایه برای تمام خطاهای درگاه پرداخت"""
    default_message = "خطای عمومی درگاه پرداخت رخ داده است"


# ==================== خطاهای ارتباطی ====================
class PaymentGatewayConnectionError(PaymentGatewayError):
    """خطا در ارتباط با درگاه پرداخت"""
    default_message = "خطا در ارتباط با درگاه پرداخت"

    def __init__(self, url=None, status_code=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.status_code = status_code


class PaymentGatewayTimeoutError(PaymentGatewayConnectionError):
    """اتصال به درگاه پرداخت زمان‌گذشت"""
    default_message = "زمان اتصال به درگاه پرداخت به پایان رسید"


class PaymentGatewayInvalidResponse(PaymentGatewayError):
    """پاسخ دریافتی از درگاه پرداخت نامعتبر است"""
    default_message = "پاسخ دریافتی از درگاه پرداخت نامعتبر است"

    def __init__(self, response_data=None, validation_errors=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_data = response_data
        self.validation_errors = validation_errors or []


# ==================== خطاهای اعتبارسنجی ====================
class PaymentValidationError(PaymentError):
    """خطای اعتبارسنجی داده‌های پرداخت"""
    default_message = "داده‌های پرداخت نامعتبر هستند"


class PaymentAmountError(PaymentValidationError):
    """خطای مربوط به مبلغ پرداخت"""
    default_message = "مبلغ پرداخت نامعتبر است"

    def __init__(self, amount=None, min_amount=None, max_amount=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = amount
        self.min_amount = min_amount
        self.max_amount = max_amount


# ==================== خطاهای درگاه‌ها ====================
class PaymentGatewayNotSupported(PaymentGatewayError):
    """درگاه پرداخت پشتیبانی نمی‌شود"""
    default_message = "درگاه پرداخت مورد نظر پشتیبانی نمی‌شود"

    def __init__(self, gateway_name=None, supported_gateways=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gateway_name = gateway_name
        self.supported_gateways = supported_gateways or []


class PaymentGatewayConfigError(PaymentGatewayError):
    """تنظیمات درگاه پرداخت ناقص است"""
    default_message = "تنظیمات درگاه پرداخت به درستی انجام نشده است"


class PaymentGatewayRejectedError(PaymentGatewayError):
    """درخواست پرداخت توسط درگاه رد شد"""
    default_message = "درخواست پرداخت توسط درگاه رد شد"

    def __init__(self, gateway_code=None, gateway_message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gateway_code = gateway_code
        self.gateway_message = gateway_message


# ==================== خطاهای تراکنش ====================
class PaymentTransactionError(PaymentError):
    """خطای پایه برای خطاهای تراکنش"""
    default_message = "خطایی در انجام تراکنش رخ داده است"


class PaymentRejectedError(PaymentTransactionError):
    """پرداخت توسط درگاه رد شد"""
    default_message = "درخواست پرداخت شما رد شد"

    def __init__(self, gateway_code=None, gateway_message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gateway_code = gateway_code
        self.gateway_message = gateway_message


class PaymentVerificationFailed(PaymentTransactionError):
    """تأیید پرداخت ناموفق بود"""
    default_message = "فرآیند تأیید پرداخت با خطا مواجه شد"

    def __init__(self, ref_id=None, amount=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ref_id = ref_id
        self.amount = amount


class PaymentAlreadyVerifiedError(PaymentVerificationFailed):
    """پرداخت قبلاً تأیید شده است"""
    default_message = "این پرداخت قبلاً تأیید شده است"


# ==================== خطاهای زرین‌پال ====================
class ZarinpalError(PaymentGatewayError):
    """خطای پایه برای زرین‌پال"""
    default_message = "خطای عمومی زرین‌پال رخ داده است"


class ZarinpalInvalidMerchantError(ZarinpalError):
    """مرچنت آیدی نامعتبر"""
    default_message = "مرچنت آیدی زرین‌پال نامعتبر است"


class ZarinpalDuplicateTransactionError(ZarinpalError):
    """تراکنش تکراری"""
    default_message = "این تراکنش قبلاً ثبت شده است"

    def __init__(self, authority=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authority = authority
