from django.contrib import admin
from .models import Person, Company, DocumentType, CompanyOwnerType, CompanyType, CompanySubject


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order_by']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyOwnerType)
class CompanyOwnerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanySubject)
class CompanySubjectAdmin(admin.ModelAdmin):
    pass
