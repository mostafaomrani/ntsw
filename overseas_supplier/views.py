from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView, ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from itertools import chain
from operator import attrgetter
from django.db.models import F


from .models import Person, Company
from .forms import PersonCreationForm, CompanyForm

User = get_user_model()


class OverSeasSuplierListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        p_q = Person.objects.filter(user=user)
        c_q = Company.objects.filter(user=user)
        combined = sorted(
            chain(p_q, c_q),
            key=attrgetter('created_at'),
            reverse=True  # برای مرتب‌سازی نزولی
        )

        return render(request, 'overseas_supplier/list.html', {'combined': combined})


class PersonCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PersonCreationForm
    model = Person
    template_name = "overseas_supplier/partials/person_form.html"
    success_url = reverse_lazy('supplier:supplier_list')
    success_message = 'شناسه فروشنده خارجی با موفقیت صادر شد'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success_url': self.success_url})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form_context = render_to_string(
                'overseas_supplier/partials/person_form.html', {'form': form}, request=self.request)
            return HttpResponse(form_context, status=400)
        return super.form_invalid(form)


class PersonJsonListView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        q = Person.objects.filter(user=user).values('pk', 'identifier')
        data = list(q)
        return JsonResponse(data=data, safe=False)


class PersonJson(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        user = self.request.user
        q = Person.objects.get(user=user, pk=id)
        data = {
            'id': q.pk,
            'first_name': q.first_name,
            'last_name': q.last_name,
            'country': q.country.name
        }
        return JsonResponse(data=data, safe=False)


class PersonJsonByIdentifer(LoginRequiredMixin, View):
    def get(self, request, identifier, *args, **kwargs):
        user = self.request.user
        q = Person.objects.filter(user=user, identifier=identifier).annotate(
            country_name=F('country__name')
        ).values(
            'pk', 'first_name', 'last_name', 'country', 'country_name')
        data = list(q)
        return JsonResponse(data=data, safe=False)


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "overseas_supplier/partials/company_form.html"
    success_url = reverse_lazy('supplier:supplier_list')
    success_message = 'شناسه‌ی فروشنده‌ی خارجی شما با موفقیت صادر گردید'
    form_class = CompanyForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success_url': self.success_url})
        return super.form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form_context = render_to_string(
                'overseas_supplier/partials/company_form.html', {'form': form}, request=self.request)
            return HttpResponse(form_context, status=400)
        return super.form_invalid(form)


class CompanyJson(LoginRequiredMixin, View):
    def get(self, request, company_id):
        user = request.user
        q = get_object_or_404(Company, user=user, pk=company_id)
        data = {
            'id': q.pk,
            'name': q.name,
            'register_number': q.register_number,
            'registered_country': q.registered_country.name,
            'address': q.address,
            'phone': q.phone
        }
        return JsonResponse(data=data, safe=False)


class CompanyJsonByIdentifier(LoginRequiredMixin, View):
    def get(self, request, identifier):
        user = request.user
        q = Company.objects.filter(user=user, identifier=identifier).annotate(
            country_name=F('registered_country__name')
        ).values(
            'pk', 'name', 'register_number', 'registered_country', 'address', 'phone', 'country_name')
        data = list(q)
        return JsonResponse(data=data, safe=False)


class CompanyJsonListView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        q = Company.objects.filter(user=user).values('pk', 'identifier')
        data = list(q)
        return JsonResponse(data=data, safe=False)
