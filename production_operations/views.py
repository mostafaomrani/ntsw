from django.shortcuts import render
from .models import productionOperations
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from anbar.models import Anbar


class ProductEzharListView(ListView):
    model = productionOperations
    template_name = 'list.html' 
    context_object_name = 'product_list'




class ProductAmarTolidMonthListView(ListView):
    model = productionOperations
    template_name = 'amar_tolid_month.html' 
    context_object_name = 'product_list'



class ProductEzharBaravadKalaListView(ListView):
    model = productionOperations
    template_name = 'ezhar_baravard_kala.html' 
    context_object_name = 'product_list'



class ProductEzharTolidKalaListView(ListView):
    model = productionOperations
    template_name = 'ezhar_tolid_steps.html' 
    context_object_name = 'product_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_anbars'] = Anbar.objects.filter(user=self.request.user)
        return context


class ProductSabtAmarEshteghalListView(ListView):
    model = productionOperations
    template_name = 'sabt_amar_eshteghal.html' 
    context_object_name = 'product_list'

