from django.shortcuts import render
from .models import productionOperations
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy



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



