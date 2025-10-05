from django.shortcuts import render
from .models import Foreintrade,DocumentTradeOperation
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from anbar.models import Anbar
from .models import AnbarItem



class DocumentTradeOperationListView(ListView):
    model = DocumentTradeOperation
    template_name = 'foreintrade/input_list.html' 
    context_object_name = 'document_trade_list'

class ForeintradeOutputListView(ListView):
    model = Foreintrade
    template_name = 'foreintrade/output_list.html' 
    context_object_name = 'foreintrade_list'

class AnbarItemsListView(ListView):
    model = AnbarItem
    template_name = 'foreintrade/output_manage_list.html'  # حتما مسیر درست باشد
    context_object_name = 'anbar_items_list'  # لیست آیتم‌ها

    def get_queryset(self):
        return AnbarItem.objects.filter(anbar__user=self.request.user).select_related('anbar', 'shenase')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_anbars'] = Anbar.objects.filter(user=self.request.user)
        # context['some_other_data'] = "می‌توانید هر کانتکس اضافی را اینجا اضافه کنید"

        return context



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