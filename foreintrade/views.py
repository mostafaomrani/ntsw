from django.shortcuts import render
from .models import Foreintrade,DocumentTradeOperation
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from anbar.models import Anbar
from .models import AnbarItem
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
from django.views import View
from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import Shenase
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .models import DocumentTradeOperation, Shenase, Anbar
import json
from django.utils import timezone
import uuid


CustomUser = get_user_model()
logger = logging.getLogger(__name__)



@method_decorator(csrf_exempt, name='dispatch')
class AddKalaView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # استخراج داده‌ها از درخواست
            shenasekala = data.get('shenasekala1')
            goroohkala = data.get('goroohkala', '')
            tabaghekala = data.get('tabaghekala', '')
            description = data.get('description', '')
            unit = data.get('unit')
            tedad = data.get('tedad')
            vahed = data.get('vahed')
            typeofsanad = data.get('typeofsanad')
            anbar_id = data.get('anbar')
            descriptionkala = data.get('description', '')
            foroshande = data.get('foroshande', '')
            melli = data.get('melli', '')
            mobile = data.get('mobile', '')
            shomaresabtsefaresh = data.get('shomaresabtsefaresh', '')
            manshaarz = data.get('manshaarz', '')
            kootaj = data.get('kootaj', '')
            shomaresanadforosh = data.get('shomaresanadforosh', '')

            # اعتبارسنجی
            if not shenasekala:
                return JsonResponse({"success": False, "error": "شناسه کالا الزامی است"})
            if not tedad:
                return JsonResponse({"success": False, "error": "تعداد/مقدار الزامی است"})
            if not vahed:
                return JsonResponse({"success": False, "error": "مبلغ واحد الزامی است"})
            if not typeofsanad:
                return JsonResponse({"success": False, "error": "نوع سند الزامی است"})
            if not anbar_id:
                return JsonResponse({"success": False, "error": "انبار الزامی است"})

            # پیدا کردن یا ایجاد Shenase
            shenase, created = Shenase.objects.get_or_create(shenase=shenasekala, defaults={
                'shenase_category_title': goroohkala or tabaghekala or 'نامشخص',
                'description': description,
                'unit': unit,
                'shenase_title': goroohkala or tabaghekala or 'نامشخص',  # فرض بر استفاده از گروه یا طبقه کالا
                'user': request.user  # افزودن کاربر فعلی به Shenase
            })

            # پیدا کردن انبار
            try:
                anbar = Anbar.objects.get(id=anbar_id)
            except Anbar.DoesNotExist:
                return JsonResponse({"success": False, "error": "انبار یافت نشد"})

            # فرض می‌کنیم seller_anbar همان anbar است
            seller_anbar = anbar

            # کاربر فعلی
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"success": False, "error": "کاربر باید وارد سیستم شده باشد"})

            # ایجاد شماره سند منحصربه‌فرد
            document_number = f"DOC-{uuid.uuid4().hex[:8]}"

            # تاریخ جاری
            current_date = timezone.now().date()

            # ایجاد سند
            document = DocumentTradeOperation.objects.create(
                document_number=document_number,
                document_date=current_date,
                delivery_date=current_date,
                register_date=current_date,
                document_type=typeofsanad,
                origin=foroshande or 'نامشخص',
                destination=anbar.name,
                bill_number=shomaresabtsefaresh or kootaj or f"BILL-{uuid.uuid4().hex[:6]}",
                description=descriptionkala,
                usable_amount=tedad,
                actual_amount=tedad,
                count_sell=tedad,
                shenase=shenase,
                unit=unit,
                operation_type='input_transfer',
                status='pending',
                anbar=anbar,
                seller_anbar=seller_anbar,
                user=user,
                seller=user,
                buyer=None
            )

            is_trackable = True  # جایگزین با منطق واقعی پروژه شما

            return JsonResponse({
                "success": True,
                "message": "کالا با موفقیت اضافه شد",
                "is_trackable": is_trackable,
                "id": document.id,
                "document_number": document_number,
                "goroohkala": goroohkala,
                "tabaghekala": tabaghekala,
                "description": description,
                "unit": unit,
                "tedad": tedad,
                "vahed": vahed
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    def get(self, request):
        return JsonResponse({"success": False, "error": "Method not allowed"})
    
    
    
class SaveTransferView(View):
    def post(self, request):
        try:
            
            # دریافت داده‌های JSON
            data = json.loads(request.body)
            
            # استخراج national_code
            national_code = data.get('national_code', '')
            seller_anbar = data.get('seller_anbar', '')
            Description = data.get('Description', '')
            Description = data.get('Description', '')
            
            # استخراج items
            items = data.get('items', [])
            
            # استخراج stuff_id و count اولین آیتم
            stuff_id = items[0].get('stuff_id', '') if items else ''
            count = items[0].get('count', '0') if items else '0'
            
            # اعتبارسنجی اولیه
            if not national_code:
                return JsonResponse({
                    'status': 'error',
                    'message': 'کد ملی الزامی است.'
                }, status=400)
            if not items:
                return JsonResponse({
                    'status': 'error',
                    'message': 'لیست آیتم‌ها الزامی است.'
                }, status=400)
            if not stuff_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'شناسه کالا الزامی است.'
                }, status=400)
            if not count.isdigit():
                return JsonResponse({
                    'status': 'error',
                    'message': 'مقدار count باید عددی باشد.'
                }, status=400)

            # پیدا کردن کاربر بر اساس username برابر با national_code
            try:
                user = CustomUser.objects.get(username=national_code)
                user_id = user.id
            except ObjectDoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'کاربری با نام کاربری {national_code} یافت نشد.'
                }, status=404)

            # آپدیت DocumentTradeOperation
            try:
                document = DocumentTradeOperation.objects.get(id=stuff_id)
                
                # تبدیل usable_amount و count به عدد
                try:
                    current_usable_amount = float(document.usable_amount) if document.usable_amount else 0
                except (ValueError, TypeError):
                    return JsonResponse({
                        'status': 'error',
                        'message': f'مقدار usable_amount ({document.usable_amount}) نامعتبر است.'
                    }, status=400)
                
                try:
                    count_value = float(count)
                except (ValueError, TypeError):
                    return JsonResponse({
                        'status': 'error',
                        'message': f'مقدار count ({count}) نامعتبر است.'
                    }, status=400)
                
                # بررسی اینکه مقدار کافی وجود داشته باشد
                if current_usable_amount < count_value:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'مقدار قابل استفاده ({current_usable_amount}) کمتر از مقدار درخواستی ({count_value}) است.'
                    }, status=400)
                
                # کسر count از usable_amount
                new_usable_amount = current_usable_amount - count_value
                document.usable_amount = str(new_usable_amount)  # تبدیل به رشته برای ذخیره
                
                # آپدیت buyer با کاربر پیدا شده
                document.buyer = user
                document.count_sell = count_value
                document.seller = request.user
                # document.destination = Description
                
                # آپدیت status (اختیاری)
                document.status = 'pending'
                document.seller_anbar_id = seller_anbar
                
                document.save()
            except ObjectDoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'سندی با شناسه {stuff_id} یافت نشد.'
                }, status=404)

            # پاسخ JSON با national_code، items، stuff_id و user_id
            return JsonResponse({
                'status': 'debug',
                'message': 'داده‌های ارسالی دریافت و سند آپدیت شد.',
                'data': data,
                'national_code': national_code,
                'items': items,
                'stuff_id': stuff_id,
                'user_id': user_id
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'داده‌های ارسالی نامعتبر هستند.'
            }, status=400)
        except IndexError:
            return JsonResponse({
                'status': 'error',
                'message': 'لیست آیتم‌ها خالی است.'
            }, status=400)
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'مقدار usable_amount یا count نامعتبر است.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'خطا: {str(e)}'
            }, status=500)
            
   
class CheckShenaseView(View):
    def get(self, request):
        shenase_id = request.GET.get('shenase', None)
        if not shenase_id:
            return JsonResponse({'error': 'شناسه کالا الزامی است'}, status=400)

        try:
            shenase = Shenase.objects.get(shenase=shenase_id)
            data = {
                'shenase_category_title': shenase.shenase_category_title,
                'description': shenase.description,
                'unit': shenase.unit,
                'unit_price': 0 
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'شناسه کالا یافت نشد'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
             

@csrf_exempt
@require_POST
def approve_document(request, pk=None):
    try:
        data = json.loads(request.body)
        pk = pk or data.get('id')

        # دریافت سند از دیتابیس
        document = DocumentTradeOperation.objects.get(pk=pk)

        # به‌روزرسانی وضعیت سند
        document.status = 'approved'
        document.bill_number = data.get('WayBillNumber')

        # بررسی انبار فروشنده
        seller_anbar_id = data.get('anbarmaghsad')
        if not seller_anbar_id:
            return JsonResponse({'success': False, 'message': 'انبار فروشنده مشخص نشده است.'})

        try:
            seller_anbar = Anbar.objects.get(pk=seller_anbar_id)
            document.seller_anbar = seller_anbar
        except Anbar.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'انبار فروشنده یافت نشد.'})

        # دریافت count_sell و تبدیل به عدد
        count_sell = data.get('count_sell')
        if count_sell is None:
            # اگر count_sell در داده‌های ارسالی نیست، از مدل دریافت کنید
            count_sell = document.count_sell
        else:
            # اطمینان از اینکه count_sell یک رشته معتبر است
            if not isinstance(count_sell, str) or not count_sell.strip():
                return JsonResponse({'success': False, 'message': 'مقدار count_sell نامعتبر است.'})

        # تبدیل count_sell به عدد
        try:
            count_sell = float(count_sell)
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting count_sell: {count_sell}, type: {type(count_sell)}")
            return JsonResponse({'success': False, 'message': f'مقدار count_sell نامعتبر است: {count_sell}'})

        # دریافت و تبدیل actual_amount به عدد
        if not document.actual_amount or not isinstance(document.actual_amount, str):
            return JsonResponse({'success': False, 'message': 'مقدار actual_amount نامعتبر است.'})

        try:
            actual_amount = float(document.actual_amount)
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting actual_amount: {document.actual_amount}, type: {type(document.actual_amount)}")
            return JsonResponse({'success': False, 'message': f'مقدار actual_amount در دیتابیس نامعتبر است: {document.actual_amount}'})

        # بررسی اینکه count_sell از actual_amount بیشتر نباشد
        if count_sell > actual_amount:
            return JsonResponse({'success': False, 'message': 'مقدار فروخته‌شده بیشتر از موجودی است.'})

        # کسر count_sell از actual_amount و تبدیل به رشته برای ذخیره
        new_actual_amount = actual_amount - count_sell
        document.actual_amount = str(new_actual_amount)  # تبدیل به رشته برای ذخیره در CharField

        # ذخیره تغییرات
        document.save()
        return JsonResponse({'success': True, 'message': 'سند با موفقیت تأیید شد.'})

    except DocumentTradeOperation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'سند یافت نشد.'})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'success': False, 'message': f'خطا: {str(e)}'}, status=500)
    
    
    
class DocumentTradeOperationListView(ListView):
    model = DocumentTradeOperation
    template_name = 'foreintrade/input_list.html'
    context_object_name = 'document_trade_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            buyer=self.request.user
        ).exclude(
           buyer='0'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anbars'] = Anbar.objects.filter(user=self.request.user)
        return context

    
    
class AnbarItemsListView(ListView):
    model = DocumentTradeOperation
    template_name = 'foreintrade/output_manage_list.html'  # حتما مسیر درست باشد
    context_object_name = 'anbar_items_list' 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_anbars'] = Anbar.objects.filter(user=self.request.user)
        # context['some_other_data'] = "می‌توانید هر کانتکس اضافی را اینجا اضافه کنید"

        return context




class ForeintradeOutputListView(ListView):
    model = DocumentTradeOperation
    template_name = 'foreintrade/output_list.html' 
    context_object_name = 'document_trade_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            seller=self.request.user
        ).exclude(
           buyer='0'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anbars'] = Anbar.objects.filter(user=self.request.user)
        return context



class ForeintradeManageKalaListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/output_manage_list.html' 
    context_object_name = 'foreintrade_list'



class ForeintradeVoroodListView(ListView):
    model = DocumentTradeOperation
    template_name = 'foreintrade/vorood_kala.html'
    context_object_name = 'documenttradeoperation_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_anbars'] = Anbar.objects.filter(user=self.request.user)

        context['documenttradeoperation_list'] = DocumentTradeOperation.objects.filter(user=self.request.user)
        return context
    

class ForeintradeKhoroojListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/vorood_khorooj_kala.html' 
    context_object_name = 'foreintrade_list'


class RegisterForeintradeKhoroojListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/register_vorood_khorooj_kala.html' 
    context_object_name = 'foreintrade_list'


class ForeintradeExcelModiriatListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/modiriat_asnad_excel.html' 
    context_object_name = 'foreintrade_list'


class ForeintradeElectronicFactorListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/electronic_factor.html' 
    context_object_name = 'foreintrade_list'


class ForeintradeMaliatSooratHesabListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/smaliat_sorathesab.html' 
    context_object_name = 'foreintrade_list'


class ForeintradeVaziatAmalkardListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/vaziat_amalkard.html' 
    context_object_name = 'foreintrade_list'



class ForeintradeBoorsKalaListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/boors_kala.html' 
    context_object_name = 'foreintrade_list'
    
class ForeintradeEzharvoroodStepListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/ezhar_vorood_steps.html' 
    context_object_name = 'foreintrade_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_anbars'] = Anbar.objects.filter(user=self.request.user)

        return context
    


class ForeintradeCreateView(CreateView):
    model = Foreintrade
    fields = '__all__'  # همه فیلدها
    # یا
    # fields = ['field1', 'field2', 'field3']  # فیلدهای خاص
    template_name = 'foreintrade/create.html'
    success_url = reverse_lazy('foreintrade:foreintrade_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ثبت سرفصل جدید'
        return context