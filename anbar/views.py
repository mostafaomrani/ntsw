from django.shortcuts import render,redirect
from .models import Anbar
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import requests


def anbar_list_view(request):

    if request.user.is_authenticated:
        anbar_list = Anbar.objects.filter(user=request.user)
    else:
        anbar_list = Anbar.objects.none() 

    context = {
        'anbar_list': anbar_list,
    }
    return render(request, 'anbar/anbar_list.html', context)

@csrf_exempt
def anbar_save(request):
    if request.method == "POST":
        
        postal_code = request.POST.get("postalCode")
        anbar_name = request.POST.get("anbarName")
        user=request.user
        user=request.user
        
        url = 'https://api.zibal.ir/v1/facility/postalCodeInquiry'
        headers = {
            'Authorization': 'Bearer efc940b60d194a63ac7e82dd0398669e'
        }
        data = {
            'postalCode': postal_code
        }

        response = requests.post(url, headers=headers, data=data)

        response_data = response.json()
        if response.status_code == 200 and response_data.get('result') == 1:
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
                
        
        address = address

        # ذخیره در دیتابیس
        Anbar.objects.create(postal_code=postal_code, name=anbar_name,user=user,address=address)

        return redirect('anbar:anbar_list')  # بعد از ذخیره دوباره صفحه لود بشه

    anbar_list = Anbar.objects.all()
    context = {
        'anbar_list': anbar_list,
    }
    return render(request, 'anbar/anbar_list.html', context)