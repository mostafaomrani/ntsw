from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DetailView, DeleteView, UpdateView
from django.http import JsonResponse, Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
import uuid

from extensions.mixins import FilterMixin
from extensions.utils import convert_currncy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    CurrencyRequest,
    Undertaking,
    FacilityLocation,
    RepaymentDeadline,
    CurrencyRate,
    SupplyCurrencyPlace,
    RequestType,
    STATUS_CHOICES,
)
from extensions.mixins import UpdateStatusMixin

from .forms import (SelectMainDataForm,
                    RequestForm,
                    CurrencyRequestDecompositionForm,
                    CurrencyRequestUpdateForm,
                    )
from order_registration.models import MainData
import os


class RequestListView(LoginRequiredMixin, ListView):
    model = CurrencyRequest
    template_name = 'currency_allocation/request_list.html'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.filter(main_data__user=self.request.user)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SelectMainDataForm(user=self.request.user)
        return context


class RequestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CurrencyRequest
    form_class = RequestForm
    template_name = 'currency_allocation/create_request.html'
    success_url = reverse_lazy('currency_allocation:requests')
    success_message = 'تخصیص ارز با موفقیت ایجاد شد'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        main_data_id = self.request.GET.get('main_data')
        main_data = get_object_or_404(MainData, pk=main_data_id, user=user)
        context['main_data'] = main_data
        return context

    def form_valid(self, form):
        user = self.request.user
        main_data_id = self.request.GET.get('main_data')
        if not main_data_id:
            return HttpResponseBadRequest("هیچ پرونده‌ای انتخاب نشده است")
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        form.instance.request_amount = convert_currncy(
            form.instance.request_amount_by_main_data_currency, main_data.financial.currency_type, form.instance.currency)
        form.instance.main_data = main_data
        form.instance.user = user
        form.save()
        return super().form_valid(form)


class UndertakingJsonListView(LoginRequiredMixin, FilterMixin, View):
    model = Undertaking
    filter_field = 'transaction_type'

    def get(self, request, transaction_type, *args, **kwargs):
        undertaking_list = self.get_filtered_data(transaction_type)
        return self.get_json_response(undertaking_list)


class FacilityLocationJsonListView(LoginRequiredMixin, FilterMixin, View):
    model = FacilityLocation
    filter_field = 'undertaking'

    def get(self, request, undertaking, *args, **kwargs):
        re_list = self.get_filtered_data(undertaking)
        return self.get_json_response(re_list)


class RepaymentDeadLineJsonListView(LoginRequiredMixin, FilterMixin, View):
    model = RepaymentDeadline
    filter_field = 'facility_location'

    def get(self, request, facility, *args, **kwargs):
        re_list = self.get_filtered_data(facility)
        return self.get_json_response(re_list)


class SupplyCurrencyPlaceJsonListView(LoginRequiredMixin, FilterMixin, View):
    model = SupplyCurrencyPlace
    filter_field = 'repayment_deadline'

    def get(self, request, repayment_deadline, *args, **kwargs):
        sc_list = self.get_filtered_data(repayment_deadline)
        return self.get_json_response(sc_list)


class CurrencyRateJsonListView(LoginRequiredMixin, FilterMixin, View):
    model = CurrencyRate
    filter_field = 'supply_currency'

    def get(self, request, currency_rate, *args, **kwargs):
        cr_list = self.get_filtered_data(currency_rate)
        return self.get_json_response(cr_list)


class RequestTypeJsonListView(LoginRequiredMixin, FilterMixin, View):
    model = RequestType
    filter_field = 'currency_rate'

    def get(self, request, currency_rate, *args, **kwargs):
        rt_list = self.get_filtered_data(currency_rate)
        return self.get_json_response(rt_list)


class RequestDetailView(DetailView):
    model = CurrencyRequest
    template_name = "currency_allocation/request_details.html"


class CurrencyRequestDecomposition(LoginRequiredMixin, View):
    def get(self, request, currency_request_pk):
        old_currency_request = get_object_or_404(
            CurrencyRequest,
            main_data__user=self.request.user,
            pk=currency_request_pk
        )
        context = {
            'form': CurrencyRequestDecompositionForm(),
            'old_currency_request': old_currency_request,
            'decomposition': old_currency_request.children.all().order_by('created_at')
        }
        return render(request, 'currency_allocation/request_decomposition.html', context)

    def post(self, request, currency_request_pk):
        old_currency_request = get_object_or_404(
            CurrencyRequest,
            main_data__user=self.request.user,
            pk=currency_request_pk
        )
        new_currency_request_row = 2
        childrens = old_currency_request.children.all()
        if childrens.exists():
            last_child = childrens.last()
            last_row = last_child.row
            new_currency_request_row = last_row + 1

        context = {
            'old_currency_request': old_currency_request
        }
        form = CurrencyRequestDecompositionForm(request.POST)
        if form.is_valid():
            new_request = form.cleaned_data.get(
                'new_currency_request'
            )
            new_currency_request = CurrencyRequest(
                main_data=old_currency_request.main_data,
                currency=old_currency_request.currency,
                request_amount_by_main_data_currency=new_request,
                request_amount=new_request,
                transaction_type=old_currency_request.transaction_type,
                undertaking=old_currency_request.undertaking,
                facility_location=old_currency_request.facility_location,
                repayment_deadline=old_currency_request.repayment_deadline,
                supply_currency_place=old_currency_request.supply_currency_place,
                currency_rate=old_currency_request.currency_rate,
                request_type=old_currency_request.request_type,
                duration_per_month=old_currency_request.duration_per_month,
                expire_date=old_currency_request.expire_date,
                document=old_currency_request.document,
                row=new_currency_request_row,
                parent_request=old_currency_request,
                user=request.user
            )
            new_currency_request.save()
            return redirect('currency_allocation:decomposition', currency_request_pk=currency_request_pk)

        context['form'] = form
        return render(
            request,
            'currency_allocation/request_decomposition.html',
            context
        )


class CurrencyRequestCanceleation(LoginRequiredMixin, View):
    def post(self, request):
        currency_request_id = request.POST.get('id')
        c_r = get_object_or_404(
            CurrencyRequest,
            main_data__user=request.user,
            pk=currency_request_id
        )
        c_r.status = 'c'
        c_r.save()
        return redirect('currency_allocation:request_detail', pk=currency_request_id)


class CurrencyRequestStatusUpdate(LoginRequiredMixin, UpdateStatusMixin, View):
    model = CurrencyRequest
    status_choices = STATUS_CHOICES
    success_message = 'وضعیت تخصیص ارز با موفقیت به روز شد.'


class CurrencyRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = CurrencyRequest
    template_name = 'currency_allocation/delete_decomposition.html'

    def get_success_url(self):
        return reverse_lazy(
            'currency_allocation:decomposition',
            kwargs={
                'currency_request_pk': self.object.parent_request.pk
            }
        )

    def get_object(self):
        obj = super(CurrencyRequestDeleteView, self).get_object()
        user = self.request.user
        main_data = obj.main_data
        print('reques:', user)
        print('main data:', main_data.user)
        if main_data.user != user:
            raise Http404
        return obj


class CurrencyRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = CurrencyRequest
    form_class = CurrencyRequestUpdateForm
    template_name = "currency_allocation/update_request.html"

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.main_data.user != user:
            raise Http404
        return obj
