from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from persiantools.jdatetime import JalaliDateTime

from .models import BusinessCard, CompanyBase, Inquiry
from datetime import datetime
from urllib.parse import urlencode




from users.models import TraderRole,Role
from django.contrib.auth.decorators import login_required

User = get_user_model()


class BusinessCardCreateView(SuccessMessageMixin, CreateView):
    model = BusinessCard
    fields = []
    success_message = 'کارت بازرگانی شما با موفقیت صادر شد'

    def get_success_url(self):
        base_url = reverse_lazy(
            'upload_qualifications:business_cards')
        query_params = {'active': 'bazorgan'}
        
        user = self.request.user
        # اضافه کردن نقش به کاربر
        role = Role.objects.get(code="bc")
        user.roles.add(role)
        user.active_role = role
        user.save()

        return f"{base_url}?{urlencode(query_params)}"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        if (user.has_business_card and user.active_role == 'br') or (user.has_company_business_card and user.active_role == 'bt'):
            messages.error(self.request, 'شما این نقش را دارید')
            return redirect('upload_qualifications:business_cards')
        if user.active_role == 'br':
            user.has_business_card = True
            form.instance.card_type = 'p'
        else:
            user.has_company_business_card = True
            form.instance.card_type = 'c'
        form.save()
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'مشکلی در صدور کارت بازرگانی شما پیش آمده است لطفا با پشتیبانی دمو تماس بگیرید.')
        return reverse_lazy('upload_qualifications:business_cards')


class BusinessCardListView(ListView):


    model = BusinessCard
    template_name = "upload_qualifications/business_card_list.html"

    def get_queryset(self):
        q = super().get_queryset()
        user = self.request.user
        card_type = 'p' if user.active_role == 'br' else 'c'

        return q.filter(user=user, card_type=card_type).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["trade_roles"] = TraderRole.objects.filter(user=self.request.user).order_by('-created_at')

        return context


class CompanyBaseCreateView(SuccessMessageMixin, CreateView):
    model = CompanyBase
    success_url = reverse_lazy('dashboard:base_role_dashboard')
    template_name = "upload_qualifications/create_company_base.html"
    success_message = 'نقش پایه‌ی حقوقی برای شما با موفقیت ایجاد شد.'
    fields = (
        'owner_type',
        'national_identifier',
        'email',
        'url',
        'fax',
        'phone',
    )

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        user.has_company_base = True
        user.save()
        return super().form_valid(form)


class ResellerIntroducingView(ListView):
    def get(self, request, *args, **kwargs):

        user = request.user
    
        print("ResellerIntroducingView")

        # داده‌های مورد نیاز برای این ویو خاص هم می‌توان اضافه کرد
        context = {
            'message': 'این ویو مخصوص تاجر است',
            # ... هر داده دیگری که نیاز داری
        }
        return render(request,"upload_qualifications/reseller-introducing-view.html", context)

@login_required
def save_trader_role(request):
    user = request.user
    if request.method == "POST":
        # گرفتن اطلاعات از فرم
        action_name = request.POST.get("actionNameStr")
        not_show_for_seller = request.POST.get("chkNotShowForSeller") == "on"
        activity_domain_id = request.POST.get("userRoleActivityID")
        activity_type_id = request.POST.get("typeActivityID")
        phone = request.POST.get("Phone")   
        postal_code = request.POST.get("postalCodeStr")
        address = request.POST.get("addressPostalCodeStr", "")

        # تعیین نقش کاربر (مثلاً کد 'it' برای تاجر)
        # if request.POST.get("typeActivityID") == "تولید کننده":
        #     role = Role.objects.get(code="bl")
        # elif request.POST.get("typeActivityID") == "وارد کننده":
        #     role = Role.objects.get(code="it")

        if  request.POST.get('role_symbol') == 'it':
            role = Role.objects.get(code="it")
        elif request.POST.get('role_symbol') == 'ih':
            role = Role.objects.get(code="ih")


        # ذخیره در جدول TraderRole
        TraderRole.objects.create(
            user=user,
            role=role,
            action_name=action_name,
            activity_domain=activity_domain_id,
            activity_type=activity_type_id,
            phone=phone,
            postal_code=postal_code,
            address=address,
            not_show_for_seller=not_show_for_seller
        )

        # اضافه کردن نقش به کاربر
        user.roles.add(role)
        user.active_role = role
        user.save()

        return redirect("upload_qualifications:business_cards")  # بعد از ذخیره صفحه را رفرش یا هدایت کن

    # GET request، فقط فرم را نمایش بده
    return render(request, "upload_qualifications/business_card_list.html")
