from django.db import models


class ProductCategory(models.Model):
    # این جدول دسته بندی کالاهای موجود در سایت است
    title = models.CharField('عنوان', max_length=100)
    description = models.CharField('توضیح', max_length=250)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی'

    def __str__(self):
        return f'دسته بندی‌ {self.title}'


class Product(models.Model):
    # این جدول کالاهای موجود در سایت را نمایش می‌دهد که کالاها از روی این جدول ساخته می‌شود
    title = models.CharField('عنوان سرفصل', max_length=250)
    en_title = models.CharField('کتگوری', max_length=250)
    featue_image = models.ImageField(
        'تصویر کالا', upload_to='uploads/product_identifier', max_length=500)
    description = models.TextField('تعریف سرفصل')
    message = models.TextField('هشدار')
    code = models.PositiveSmallIntegerField('کد سرفصل')
    gtin = models.JSONField('شناسه جهانی کالا(GTIN)')
    hs = models.JSONField('کد HS')
    isic = models.JSONField('کد ISIC')
    count_unit = models.JSONField('واحد شمارش')
    mandatory_descriptive_field = models.JSONField('فیلدهای توصیفی اجباری')
    optional_fields = models.JSONField('فیلدهای اختیاری')
    category = models.ManyToManyField(
        ProductCategory, verbose_name='دسته‌بندی(ها)')

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا'

    def __str__(self):
        return self.title


class ProductIdentifier(models.Model):
    # این جدول برای کالاهایی است که کالا برای آنها گرفته شده است
    gtin = models.CharField('شناسه جهانی قلم کالا',
                            max_length=100, default=None, blank=True)
    hs_code = models.CharField('کد HS', max_length=100)  # required field
    isic = models.CharField('کد ISIC', max_length=100,
                            default=None, blank=True)
    cpc = models.CharField('کد CPC', max_length=100, default=None, blank=True)
    identitie = models.PositiveSmallIntegerField(
        'شناسه', default=None, blank=True)
    mandatory_descriptive_field = models.JSONField('فیدهای توصیفی اجباری')
    optional_fields = models.JSONField('فیلدهای اختیاری')
    count_unit = models.CharField('واحد شمارش', max_length=50)

    class Meta:
        verbose_name = 'شناسه کالا'
        verbose_name_plural = 'شناسه کالا'

    def __str__(self):
        return self.name
