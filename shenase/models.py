from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Shenase(models.Model):
    shenase_category_id = models.CharField(max_length=100, blank=True, null=True)
    shenase_category_title = models.CharField(max_length=100, blank=True, null=True)
    shenase = models.CharField(max_length=255, blank=True, null=True)
    shenase_title = models.CharField(max_length=255, blank=True, null=True)
    shenase_international = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    hs = models.CharField(max_length=255, blank=True, null=True)
    category_policy_identities = models.CharField(max_length=255, blank=True, null=True)
    cpc = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    isic = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shenases', blank=True, null=True)
    
    class Meta:
        db_table = "shenase"

    def __str__(self):
        return f"{self.title} ({self.category_title})"

class Document(models.Model):
    TYPE_CHOICES = (
        ("1", "تصویر"),
        ("2", "مستندات فنی"),
    )

    file = models.FileField(upload_to="uploads/")   # مسیر ذخیره داخل MEDIA_ROOT/uploads/
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"   # 👈 اسم جدول دقیقا documents خواهد بود

    def __str__(self):
        return f"{self.get_type_display()} - {self.file.name}"

class ShenaseCategory(models.Model):  # دسته‌بندی
    name = models.CharField(max_length=255, verbose_name="نام دسته‌بندی")

    class Meta:
        db_table = "shenase_category"
        verbose_name = "دسته‌بندی شناسه"
        verbose_name_plural = "دسته‌بندی‌های شناسه"

    def __str__(self):
        return self.name


class Syllabus(models.Model):  # سرفصل
    category = models.ForeignKey(ShenaseCategory, on_delete=models.CASCADE, related_name="syllabuses")
    code = models.CharField(max_length=50, unique=True, verbose_name="کد سرفصل")
    title = models.CharField(max_length=255, verbose_name="عنوان سرفصل")
    description = models.CharField(max_length=255, verbose_name=" تعریف سرفصل ")
    title_en = models.CharField(max_length=255, verbose_name="نام انگلیسی")
    image = models.ImageField(upload_to="syllabus_images/", null=True, blank=True, verbose_name="تصویر کالا")

    class Meta:
        db_table = "syllabus"

    def __str__(self):
        return f"{self.title} ({self.code})"


class HS(models.Model):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name="hs_list")
    name = models.CharField(max_length=255, verbose_name="نام")
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.SET_NULL, related_name='children')
    code = models.CharField(max_length=50, unique=True, verbose_name="کد hs")

    class Meta:
        db_table = "hs"

    def __str__(self):
        return self.name


class ISIC(models.Model):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name="isic_list")
    name = models.CharField(max_length=255, verbose_name="نام")
    code = models.CharField(max_length=50, unique=True, verbose_name="کد isic")


    class Meta:
        db_table = "isic"

    def __str__(self):
        return self.name



class RequiredField(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    ValueName = models.CharField(max_length=255, verbose_name="نام انگلیسی")
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name="isic_list")



    class Meta:
        db_table = "shenase_required_field"

    def __str__(self):
        return self.title



class OptionalField(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    ValueName = models.CharField(max_length=255, verbose_name="نام انگلیسی")
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, related_name="isic_list")



    class Meta:
        db_table = "shenase_optional_field"

    def __str__(self):
        return self.title



class ShenaseFieldValues(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="شناسه")
    shenase_field = models.ForeignKey(
        RequiredField,
        on_delete=models.CASCADE,
        related_name="field_values",
        verbose_name="فیلد الزامی"
    )
    title = models.CharField(max_length=255, verbose_name="عنوان")
    en_title = models.CharField(max_length=255, verbose_name="عنوان انگلیسی")

    class Meta:
        db_table = "shenase_field_values"
        verbose_name = "مقدار فیلد شناسه"
        verbose_name_plural = "مقادیر فیلدهای شناسه"

    def __str__(self):
        return f"{self.title} ({self.en_title})"