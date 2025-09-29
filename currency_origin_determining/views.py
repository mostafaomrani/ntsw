from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.forms import inlineformset_factory
from django.http import Http404
from order_registration.models import MainData
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Banking,
    Ware,
    WithoutCurrencyTransfer,
    WithoutCurrencyTransferWare,
    STATUS_CHOICES,
)
from .forms import (
    SelectMainDataForm,
    BankingForm,
    LadingBillingFormSet,
    WareForm,
    SelectMainDataFormForWithoutCurrencyTransfer,
    WithoutCurrencyTransferForm,
    WithoutCurrencyTransferLadingBillingFormSet,
    WithoutCurrencyTransferWareForm,
)
from extensions.mixins import UpdateStatusMixin
from django.contrib.messages.views import SuccessMessageMixin


class BankingListView(LoginRequiredMixin, ListView):
    model = Banking

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(main_data__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SelectMainDataForm(user=self.request.user)
        return context


class BankingCreateView(LoginRequiredMixin, CreateView):
    model = Banking
    form_class = BankingForm
    template_name = "currency_origin_determining/create_banking.html"
    success_url = reverse_lazy('currency_origin_determining:banking_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_data = self.main_data
        context["main_data"] = main_data
        ware_set = main_data.ware_set.all()
        # Daynamic ware form set
        WareFormSet = inlineformset_factory(
            Banking,
            Ware,
            form=WareForm,
            extra=max(1, len(ware_set)),
            can_delete=True
        )
        ware_formset = WareFormSet(queryset=ware_set)
        combined_ware_formset = zip(ware_set, ware_formset)
        context['combined_ware_formset'] = combined_ware_formset
        if self.request.POST:
            context['lading_bill_formset'] = LadingBillingFormSet(
                self.request.POST)
            context['ware_formset'] = WareFormSet(self.request.POST)
        else:
            context['lading_bill_formset'] = LadingBillingFormSet()
            context['ware_formset'] = WareFormSet()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        main_data_id = self.request.GET.get("main_data")
        user = self.request.user
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        self.main_data = main_data
        kwargs['main_data'] = self.main_data
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        laiding_bill_form_set = context['lading_bill_formset']
        ware_form_set = context['ware_formset']
        print(context)
        print('-------')
        print(ware_form_set)
        user = self.request.user
        main_data_id = self.request.GET.get('main_data')
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        form.instance.main_data = main_data
        form.instance.user = user
        if laiding_bill_form_set.is_valid() and form.is_valid():
            self.object = form.save()
            # ذخیره بارنامه‌ها
            laiding_bill_form_set.instance = self.object
            laiding_bill_form_set.save()
            # ذخیره فقط فرم‌هایی از ware که چک شده‌اند
            for ware_form in ware_form_set:
                # بررسی معتبر بودن فرم و نادیده گرفتن فرم‌های خالی
                print(ware_form.is_valid())
                print(ware_form.has_changed())
                if ware_form.is_valid() and ware_form.has_changed():
                    if ware_form.cleaned_data.get('DELETE', False):
                        ware_form.instance.banking = self.object
                        ware_form.save()
                else:
                    return self.form_invalid(form)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class WithoutCurrencyTransferListView(LoginRequiredMixin, ListView):
    model = WithoutCurrencyTransfer
    template_name = "currency_origin_determining/without_currency_transfer_list.html"

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(main_data__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SelectMainDataFormForWithoutCurrencyTransfer(
            user=self.request.user
        )
        return context


class WithoutCurrencyTransferCreateView(LoginRequiredMixin, CreateView):
    model = WithoutCurrencyTransfer
    form_class = WithoutCurrencyTransferForm
    template_name = "currency_origin_determining/create_without_currency_transfer.html"
    success_url = reverse_lazy(
        'currency_origin_determining:without_currency_transfer_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_data_id = self.request.GET.get('main_data')
        main_data = get_object_or_404(
            MainData,
            user=self.request.user,
            pk=main_data_id
        )
        ware_set = main_data.ware_set.all()
        # Dynamic ware form set

        WareFormSet = inlineformset_factory(
            WithoutCurrencyTransfer,
            WithoutCurrencyTransferWare,
            form=WithoutCurrencyTransferWareForm,
            extra=max(1, len(ware_set)),
            can_delete=True
        )
        ware_formset = WareFormSet(queryset=ware_set)
        combined_ware_formset = zip(ware_set, ware_formset)
        context['combined_ware_formset'] = combined_ware_formset
        if self.request.POST:
            context['lading_bill_formset'] = WithoutCurrencyTransferLadingBillingFormSet(
                self.request.POST)
            context['ware_formset'] = WareFormSet(self.request.POST)
        else:
            context['lading_bill_formset'] = WithoutCurrencyTransferLadingBillingFormSet()
            context['ware_formset'] = WareFormSet()
        context['main_data'] = main_data
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        main_data_id = self.request.GET.get("main_data")
        user = self.request.user
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        kwargs['main_data'] = main_data
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        laiding_bill_form_set = context['lading_bill_formset']
        ware_form_set = context['ware_formset']
        user = self.request.user
        main_data_id = self.request.GET.get('main_data')
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        form.instance.main_data = main_data
        form.instance.user = user
        if laiding_bill_form_set.is_valid() and form.is_valid():
            self.object = form.save()
            # ذخیره بارنامه‌ها
            laiding_bill_form_set.instance = self.object
            # print(laiding_bill_form_set.instance.tracking_code)
            laiding_bill_form_set.save()
            # ذخیره فقط فرم‌هایی از ware که چک شده‌اند
            for ware_form in ware_form_set:
                # بررسی معتبر بودن فرم و نادیده گرفتن فرم‌های خالی
                if ware_form.is_valid() and ware_form.has_changed():
                    # بررسی اینکه تیک خورده یا نه اگر تیک بخورد یعنی کاربر برای ذخیره شدن انتخاب کرده
                    if ware_form.cleaned_data.get('DELETE', False):
                        ware_form.instance.without_currency_transfer = self.object
                        ware_form.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class CurrencyOriginDeterminingDetailMixi(LoginRequiredMixin, DetailView):
    model = None
    template_name = None

    def get_queryset(self):
        q = super().get_queryset()
        q = q.filter(user=self.request.user)
        if not q:
            raise Http404
        return q


class BankingDetailView(CurrencyOriginDeterminingDetailMixi, LoginRequiredMixin):
    model = Banking
    template_name = "currency_origin_determining/banking_detail.html"


class WithoutCurrencyTransferDetail(CurrencyOriginDeterminingDetailMixi, LoginRequiredMixin):
    model = WithoutCurrencyTransfer
    template_name = "currency_origin_determining/without_currency_transfer_detail.html"


class BankingStatusUpdate(UpdateStatusMixin, LoginRequiredMixin, View):
    model = Banking
    status_choices = STATUS_CHOICES
    success_message = 'وضعیت منشا ارز با موفقیت به روز رسانی شد'


class WithoutCurrencyTransferStatusUpdate(UpdateStatusMixin, LoginRequiredMixin, View):
    model = WithoutCurrencyTransfer
    status_choices = STATUS_CHOICES
    success_message = 'وضعیت منشا ارز با موفقیت به روز رسانی شد'
