from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from persiantools.jdatetime import JalaliDateTime
from django.views.decorators.csrf import csrf_exempt
from .models import BusinessCard, CompanyBase, Inquiry
from datetime import datetime
from urllib.parse import urlencode
import requests
from django.shortcuts import get_object_or_404


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
        
        role = Role.objects.get(code="bc")
        user.roles.add(role)
        
        user.active_role = role

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


@login_required
def delete_trader_role(request):
    if request.method == 'POST':
        try:
            # دریافت ID نقش از درخواست
            role_id = request.POST.get('role_id')
            if not role_id:
                return JsonResponse({
                    'success': False,
                    'error': 'شناسه نقش مشخص نشده است'
                }, status=400)

            # پیدا کردن نقش و بررسی مالکیت
            trader_role = get_object_or_404(TraderRole, id=role_id, user=request.user)

            # حذف نقش از دیتابیس
            trader_role.delete()

            # حذف نقش از لیست نقش‌های کاربر (اگر لازم است)
            if trader_role.role in request.user.roles.all():
                request.user.roles.remove(trader_role.role)
                # اگر نقش حذف‌شده نقش فعال کاربر بود، نقش فعال را پاک می‌کنیم
                if request.user.active_role == trader_role.role:
                    request.user.active_role = None
                    request.user.save()

            return JsonResponse({
                'success': True,
                'message': 'نقش با موفقیت حذف شد'
            })

        except TraderRole.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'نقش یافت نشد یا متعلق به شما نیست'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'فقط درخواست‌های POST مجاز هستند'
    }, status=405)
    
    
@csrf_exempt
def get_address_by_postal_code(request):
    if request.method == 'POST':
        try:
            # دریافت کد پستی از درخواست
            postal_code = request.POST.get('postal_code')
            if not postal_code or len(postal_code) != 10 or not postal_code.isdigit():
                return JsonResponse({
                    'success': False,
                    'error': 'کد پستی باید 10 رقمی و عددی باشد'
                }, status=400)

            url = 'https://api.zibal.ir/v1/facility/postalCodeInquiry'
            headers = {
                'Authorization': 'Bearer efc940b60d194a63ac7e82dd0398669e'
            }
            data = {
                'postalCode': postal_code
            }

            response = requests.post(url, headers=headers, data=data)

            # بررسی پاسخ API
            response_data = response.json()
            if response.status_code == 200 and response_data.get('result') == 1:
                # موفقیت: استخراج آدرس
                address_data = response_data.get('data', {}).get('address', {})
                address = (
                    f"{address_data.get('province', '')}, "
                    f"{address_data.get('town', '')}, "
                    f"{address_data.get('district', '')}, "
                    f"{address_data.get('street', '')}, "
                    f"{address_data.get('street2', '')}, "
                    f"شماره {address_data.get('number', '')}, "
                    f"طبقه {address_data.get('floor', '')}, "
                    f"{address_data.get('description', '')}"
                ).strip(', ')

                return JsonResponse({
                    'success': True,
                    'address': address
                })
            else:
                error_message = response_data.get('message', 'خطای نامشخص در API زیبال')
                return JsonResponse({
                    'success': False,
                    'error': error_message
                }, status=400)

        except requests.RequestException as e:
            # خطا در ارتباط با API
            return JsonResponse({
                'success': False,
                'error': f'خطا در ارتباط با API: {str(e)}'
            }, status=500)
        except Exception as e:
            # خطاهای عمومی
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'فقط درخواست‌های POST مجاز هستند'
    }, status=405)