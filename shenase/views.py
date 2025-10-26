# views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from .models import ShenaseCategory,Syllabus,HS,ISIC,Document,Shenase,RequiredField,OptionalField,ShenaseFieldValues
from django.views.generic import TemplateView
import random
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def edit_field(request):
    if request.method == 'POST':
        try:
            data_id = request.POST.get('data_id')

            if not data_id:
                return JsonResponse({
                    'success': False,
                    'message': 'sylabus_id و data_id الزامی هستند'
                }, status=400)

            try:
                field = RequiredField.objects.get(id=data_id)
            except RequiredField.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'فیلد یافت نشد'
                }, status=404)

            values = ShenaseFieldValues.objects.filter(shenase_field=field)
            values_list = [
                {
                    'id': value.id,                    
                    'value': value.title,  
                    'en_title': value.en_title,
                } for value in values
            ]

            return JsonResponse({
                'success': True,
                'values': values_list,
                'field_title': field.title,
                'latin_field_title': field.ValueName
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در پردازش درخواست: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'message': 'فقط درخواست‌های POST مجاز هستند'
        }, status=405)
        
          
import random

def generate_13_digit():
    prefix = random.choice(["28", "29"])
    zeros = "00000"
    rest_of_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return prefix + zeros + rest_of_code


def save_shenase(request):
    if request.method == "POST":
        try:
            shenase_code = generate_13_digit()
            while Shenase.objects.filter(shenase=shenase_code).exists():
                shenase_code = generate_13_digit()

            shenase = Shenase.objects.create(
                shenase_category_id = request.POST.get("shenase_category_id"),
                shenase_category_title = request.POST.get("shenase_category_title"),
                shenase_title = request.POST.get("shenase_title"),
                hs = request.POST.get("hsdata"),
                category_policy_identities = request.POST.get("categoryPolicyIdentitiesdata"),
                cpc = request.POST.get("cpcdata"),
                unit = request.POST.get("unitdata"),
                isic = request.POST.get("isicdata"),
                description = '(' + request.POST.get("shenase_category_title") + ') ' + request.POST.get("unitdata") + ' - ' + request.POST.get("required_values") ,
                shenase = shenase_code,
                user=request.user
            )

            # چاپ تست در سرور
            print("رکورد ذخیره شد ✅", shenase_code)
            
            # ریدایرکت به لیست
            return redirect('shenase:shenase_list')

        except Exception as e:
            # خطا را برگردان به کاربر به صورت JSON
            return JsonResponse({"error": str(e)}, status=500)

    # اگر روش غیر POST بود
    return JsonResponse({"error": "فقط POST مجاز است"}, status=405)




def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("inputDocumentsFile")
        description = request.POST.get("descriptionFile")
        sell_buy = request.POST.get("sellBuy")

        if not file:
            return JsonResponse({"error": "هیچ فایلی انتخاب نشده"}, status=400)
        doc = Document.objects.create(
            file=file,
            description=description,
            type=sell_buy
        )

        return JsonResponse({
            "message": "فایل با موفقیت آپلود شد",
            "file_url": doc.file.url,   # 👈 مسیر اینترنتی (مثلاً /media/uploads/test.png)
            "id": doc.id,
        })

    return JsonResponse({"error": "فقط POST مجاز است"}, status=405)



class ShenaseListView(ListView):
    model = Shenase
    template_name = 'shenase/list.html'  # مسیر قالب لیست
    context_object_name = 'shenase_categories'  # داده‌های دسته‌ها

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن داده‌های Shenase
        context['shenase_list'] = Shenase.objects.all().order_by('-created_at')
        return context

class ShenaseCreateView(CreateView):
    model = ShenaseCategory
    fields = '__all__'
    template_name = 'shenase/create.html'
    success_url = reverse_lazy('shenase:shenase_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ثبت سرفصل جدید'

        categories = ShenaseCategory.objects.all()


        context['categories'] = categories
        
        return context
    
class ShenaseDataView(View):
    def get(self, request, type=None):
        # type همون shenaseId هست
        shenase_id = type
        # print("شناسه کلیک شده:", shenase_id)

        syllabus_items = Syllabus.objects.filter(category_id=shenase_id)

        data_list = []
        for item in syllabus_items:
            print(item.title_en)
            image_url = ''
            if item.image:
                # چک می‌کنیم آیا image خودش با http یا https شروع میشه
                if str(item.image).startswith('http://') or str(item.image).startswith('https://'):
                    image_url = str(item.image)  # همین URL کامل را استفاده کن
                else:
                    # اگه مسیر نسبی بود، آدرس کامل درست کنیم
                    image_url = request.build_absolute_uri(item.image.url)

            data_list.append({
                "id": str(item.id),
                "category_id": str(item.category_id),
                "CategoryCode": item.code,
                "title": item.title,
                "title_en": item.title_en,
                "image": image_url
            })

        response_data = {
            "draw": 5,
            "recordsTotal": len(data_list),
            "Phone": None,
            "recordsFiltered": len(data_list),
            "data": data_list,
            "extraData": None
        }

        return JsonResponse(response_data)
    

class ShenaseOneDataView(View):
    def get(self, request, id=None):
        try:
            item = Syllabus.objects.get(id=id)
            hs = list(HS.objects.filter(syllabus_id=id).values('id', 'name', 'parent_id','code'))
            isic = list(ISIC.objects.filter(syllabus_id=id).values('id', 'name','code'))
            ReqField = list(RequiredField.objects.filter(syllabus_id=id).values('id', 'title','ValueName'))
            OptionField = list(OptionalField.objects.filter(syllabus_id=id).values('id', 'title','ValueName'))

            if item.image:
                if str(item.image).startswith('http://') or str(item.image).startswith('https://'):
                    image_url = str(item.image)
                else:
                    image_url = request.build_absolute_uri(item.image.url)
            else:
                image_url = ''

            response_data = {
                "id": item.id,
                "code": item.code,      
                "title": item.title,
                "title_en": item.title_en,
                "description": item.description,
                "image": image_url,
                "hs": hs,
                "isic" : isic,
                "requiredField" : ReqField,
                "optionalField" : OptionField
            }

            return JsonResponse(response_data)

        except Syllabus.DoesNotExist:
            return JsonResponse({"error": "Syllabus not found"}, status=404)





class ShenaseTransactionsView(TemplateView):
    model = ShenaseCategory
    template_name = 'shenase/in_trasactions.html'
    context_object_name = 'shenase_list'