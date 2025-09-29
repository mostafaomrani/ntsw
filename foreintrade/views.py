from django.shortcuts import render
from .models import Foreintrade
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
# Create your views here.



class ForeintradeInputListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/input_list.html' 
    context_object_name = 'foreintrade_list'

class ForeintradeOutputListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/output_list.html' 
    context_object_name = 'foreintrade_list'

class ForeintradeManageKalaListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/output_manage_list.html' 
    context_object_name = 'foreintrade_list'



class ForeintradeVoroodListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/vorood_kala.html' 
    context_object_name = 'foreintrade_list'

class ForeintradeKhoroojListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/vorood_khorooj_kala.html' 
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