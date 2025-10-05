from django.shortcuts import render,redirect
from .models import Anbar
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt


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
        address = "تهران - ایران"

        # ذخیره در دیتابیس
        Anbar.objects.create(postal_code=postal_code, name=anbar_name,user=user,address=address)

        return redirect('anbar:anbar_list')  # بعد از ذخیره دوباره صفحه لود بشه

    anbar_list = Anbar.objects.all()
    context = {
        'anbar_list': anbar_list,
    }
    return render(request, 'anbar/anbar_list.html', context)