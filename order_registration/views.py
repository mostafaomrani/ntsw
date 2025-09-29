import json
import logging
import os
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, View, ListView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import render_to_string
from persiantools.jdatetime import JalaliDate

from extensions.mixins import FilterMixin
from extensions.utils import generate_random_number
from django.contrib import messages

from .models import (
    MainData,
    CustomsAndShipping,
    ShippingType,
    EntranceEdge,
    Custom,
    Financial,
    Ware,
    BankBranch,
    CurrencySupply,
)

from .forms import (
    MainDataForm,
    CustomsAndShippingForm,
    FinancialForm,
    WareForm,
    MainDataUploadDocumentForm,
)
from overseas_supplier.models import Person, Company

from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


logger = logging.getLogger('myproject.custom')


class MainDataListView(LoginRequiredMixin, ListView):
    model = MainData
    template_name = "order_registration/main_data_list.html"

    def get_queryset(self):
        q = super().get_queryset()
        user = self.request.user
        q = q.filter(user=user)
        return q


@method_decorator(never_cache, name='dispatch')
class MainDataCreateView(LoginRequiredMixin, CreateView):
    model = MainData
    form_class = MainDataForm
    template_name = 'order_registration/create_main_data.html'

    def get_success_url(self):
        obj = self.object
        if hasattr(obj, 'custom_and_shipping'):
            # forward to edit view
            return reverse_lazy('order_registration:update_customs_and_shipping', kwargs={'pk': obj.custom_and_shipping.pk})
        return reverse_lazy('order_registration:create_customs_and_shipping', kwargs={'main_data_id': self.pk})

    def form_valid(self, form):
        object_id = form.cleaned_data['related_object_id']
        supplier_type = form.cleaned_data['supplier']
        form.instance.user = self.request.user
        form.instance.object_id = object_id
        if supplier_type == 'person':
            form.instance.supplier_type = ContentType.objects.get_for_model(
                Person)
        elif supplier_type == 'company':
            form.instance.supplier_type = ContentType.objects.get_for_model(
                Company)
        item = form.save()
        self.pk = item.pk
        response = super().form_valid(form)
        return response


@method_decorator(never_cache, name='dispatch')
class MainDataUpdateView(LoginRequiredMixin, UpdateView):
    model = MainData
    form_class = MainDataForm
    template_name = 'order_registration/update_main_data.html'

    def get_success_url(self):
        obj = self.object
        if hasattr(obj, 'custom_and_shipping'):
            # forward to edit view
            return reverse_lazy('order_registration:update_customs_and_shipping', kwargs={'pk': obj.custom_and_shipping.pk})
        return reverse_lazy('order_registration:create_customs_and_shipping', kwargs={'main_data_id': obj.pk})

    def get_initial(self):
        # دریافت مقدار اولیه از ویو والد
        initial = super().get_initial()

        # تنظیم مقدار اولیه برای فیلد supplier
        # self.object شیء مورد نظر است
        initial['supplier'] = self.object.supplier_type.model
        initial['related_object_id'] = self.object.related_object.identifier
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['order_registration_case'].widget.attrs['readonly'] = True
        return form


@method_decorator(never_cache, name='dispatch')
class CustomsAndShippingCreateView(LoginRequiredMixin, CreateView):
    model = CustomsAndShipping
    form_class = CustomsAndShippingForm
    template_name = "order_registration/create_customs_and_shipping.html"

    def dispatch(self, request, *args, **kwargs):
        main_data_id = kwargs.get('main_data_id')
        if CustomsAndShipping.objects.filter(main_data_id=main_data_id).exists():
            custom_and_shipping = CustomsAndShipping.objects.get(
                main_data_id=main_data_id)
            return redirect('order_registration:update_customs_and_shipping', pk=custom_and_shipping.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        main_data = self.object.main_data
        obj = self.object
        if (hasattr(obj.main_data, 'financial')):
            # redirect to update financial
            return reverse_lazy(
                'order_registration:update_financial',
                kwargs={'pk': obj.main_data.financial.pk}
            )

        return reverse_lazy('order_registration:create_financial', kwargs={'main_data_id': self.main_data_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        main_data_id = self.kwargs['main_data_id']
        context["main_data"] = get_object_or_404(
            MainData, user=user, pk=main_data_id)
        return context

    def form_valid(self, form):
        main_data_id = self.kwargs['main_data_id']
        user = self.request.user
        main_data = get_object_or_404(
            MainData, user=user, pk=main_data_id)
        if hasattr(main_data, 'custom_and_shipping'):
            return redirect('order_registraion:update_customs_and_shipping', pk=main_data.custom_and_shipping.pk)

        form.instance.main_data = main_data
        form.save()
        self.main_data_id = main_data.pk
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class CustomsAndShippingUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomsAndShipping
    form_class = CustomsAndShippingForm
    template_name = "order_registration/update_customs_and_shipping.html"

    def get_success_url(self):
        obj = self.object
        if (hasattr(obj.main_data, 'financial')):
            # redirect to update financial
            return reverse_lazy(
                'order_registration:update_financial',
                kwargs={'pk': obj.main_data.financial.pk}
            )
        return reverse_lazy(
            'order_registration:create_financial',
            kwargs={'main_data_id': obj.main_data.pk}
        )


@method_decorator(never_cache, name='dispatch')
class ModelUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomsAndShipping
    template_name = "order_registration/create_custom_and_shipping.html"


class ShippingJsonList(View):
    def get(self, request, incoterms_id, *args, **kwargs):
        q = ShippingType.objects.filter(
            incoterms__id=incoterms_id).values('pk', 'title')
        data = list(q)
        return JsonResponse(data=data, safe=False)


class EntranceEdgeJsonList(LoginRequiredMixin, View):
    def get(self, request, shipping_type_id=None, *args, **kwargs):
        if shipping_type_id:
            q = EntranceEdge.objects.filter(
                shipping_type__id=shipping_type_id).values('pk', 'title')
        else:
            ids = request.GET.getlist('ids[]')
            # ids = [int(id) for id in ids]
            q = EntranceEdge.objects.filter(
                shipping_type__id__in=ids).values('pk', 'title')
        data = list(q)
        return JsonResponse(data=data, safe=False)


class CustomJsonList(LoginRequiredMixin, View):
    def get(self, request, entrance_id=None, *args, **kwargs):
        if entrance_id:
            q = Custom.objects.filter(
                shipping_type__id=entrance_id).values('pk', 'title')
        else:
            ids = request.GET.getlist('ids[]')
            q = Custom.objects.filter(
                shipping_type__in=ids).values('pk', 'title')
        data = list(q)
        return JsonResponse(data=data, safe=False)


@method_decorator(never_cache, name='dispatch')
class FinancialCreateView(LoginRequiredMixin, CreateView):
    model = Financial
    template_name = "order_registration/create_financial.html"
    form_class = FinancialForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.main_data_id = kwargs.get('main_data_id')
        self.main_data = get_object_or_404(
            MainData,
            user=self.request.user,
            pk=self.main_data_id
        )

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self.main_data, 'financial'):
            return redirect(reverse_lazy(
                'order_registration:update_financial',
                kwargs={'pk': self.main_data.financial.pk}
            ))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('order_registration:ware_list', kwargs={'main_data_id': self.main_data_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_data"] = self.main_data
        return context

    def form_valid(self, form):
        form.instance.main_data = self.main_data
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.main_data, 'custom_and_shipping'):
            kwargs['has_shipping_cost'] = self.main_data.custom_and_shipping.incoterms.has_shipping_cost
        return kwargs


@method_decorator(never_cache, name='dispatch')
class FinancialUpdateView(LoginRequiredMixin, UpdateView):
    model = Financial
    form_class = FinancialForm
    template_name = "order_registration/update_financial.html"

    def get_success_url(self):
        return reverse_lazy('order_registration:ware_list', kwargs={'main_data_id': self.object.main_data.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = self.object
        main_data = obj.main_data
        if hasattr(main_data, 'custom_and_shipping'):
            kwargs['has_shipping_cost'] = main_data.custom_and_shipping.incoterms.has_shipping_cost
        return kwargs


class BankBranchJsonView(LoginRequiredMixin, View):
    def get(self, request, bank_id, *args, **kwargs):
        branch = BankBranch.objects.filter(bank=bank_id).values('id', 'title')
        branch = list(branch)
        return JsonResponse(data=branch, safe=False)


class WareListView(LoginRequiredMixin, ListView):
    model = Ware
    template_name = "order_registration/ware_list.html"

    def get_queryset(self):
        q = super().get_queryset()
        user = self.request.user
        main_data_id = self.kwargs.get('main_data_id', None)
        q = q.filter(main_data__user=user, main_data__id=main_data_id)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_data_id = self.kwargs.get('main_data_id', None)
        user = self.request.user
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        context['main_data'] = main_data
        return context


class WareCreateView(LoginRequiredMixin, CreateView):
    model = Ware
    template_name = "order_registration/partials/create_ware_form.html"
    form_class = WareForm

    def get_success_url(self):
        return reverse_lazy('order_registration:ware_list', kwargs={'main_data_id': self.main_data_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_data_id"] = self.kwargs['main_data_id']
        return context

    def form_valid(self, form):
        user = self.request.user
        main_data_id = self.kwargs.get('main_data_id')
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        form.instance.main_data = main_data
        main_data.save()
        form.save()
        self.main_data_id = main_data.pk
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success_url': self.get_success_url()})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            main_data_id = self.kwargs.get('main_data_id')
            form_context = render_to_string(
                'order_registration/partials/create_ware_form.html',
                {
                    'form': form,
                    'main_data_id': main_data_id
                },
                request=self.request
            )
            return HttpResponse(form_context, status=400)
        return super().form_invalid(form)


class WareDeleteView(LoginRequiredMixin, DeleteView):
    model = Ware
    template_name = "order_registration/delete-ware.html"

    def get_success_url(self):
        return reverse_lazy('order_registration:ware_list', kwargs={'main_data_id': self.main_data_id})

    def get_object(self, queryset=None):
        obj = super(WareDeleteView, self).get_object()
        self.main_data_id = obj.main_data_id
        if not obj.main_data.user == self.request.user:
            raise Http404
        return obj


class MainDataUploadDocumentView(LoginRequiredMixin, UpdateView):
    model = MainData
    form_class = MainDataUploadDocumentForm
    template_name = "order_registration/upload_document.html"

    def get_success_url(self):
        return reverse_lazy('order_registration:upload_document', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_data_id'] = self.kwargs['pk']
        obj = self.object
        obj.status = 'n'
        obj.save()
        file_instance = self.object.document
        if file_instance:
            filename = file_instance.name.lower()
            context['is_image'] = filename.endswith(('.jpg', '.jpeg', '.png'))
            context['is_pdf'] = filename.endswith('.pdf')
            context['url'] = file_instance.url
        return context

    def get_object(self):
        obj = super(MainDataUploadDocumentView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class MainDataDetailView(LoginRequiredMixin, DetailView):
    model = MainData
    template_name = "order_registration/detail.html"

    def get_object(self):
        obj = super(MainDataDetailView, self).get_object()
        if obj.user != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choices = MainData.STATUS_CHOICES
        obj = context['object']
        flag = True
        active = False
        statuses = []
        completion_url = reverse_lazy(
            'order_registration:upload_document',
            kwargs={
                'pk': obj.pk
            }
        )
        i = 0
        for ch in choices:
            i += 1
            if obj.status == ch[0]:  # current status for use in template breadcrumbs
                active = True
                flag = False
            if ch[0] == 'c':
                break
            statuses.append({
                'name': ch[1],
                'amount': ch[0],
                'active': active,
                'flag': flag,
                'number': i
            }
            )
            if obj.status == ch[0]:
                active = False
        if obj.status == 'n':  # if current status is new compelition_url is ware list
            completion_url = reverse_lazy(
                'order_registration:ware_list',
                kwargs={
                    'main_data_id': obj.pk
                }
            )
        elif obj.status == 'd':  # if current status is draf decide user drop
            if not hasattr(obj, 'custom_and_shipping'):
                completion_url = reverse_lazy(
                    'order_registration:create_customs_and_shipping',
                    kwargs={
                        'main_data_id': obj.pk
                    }
                )
            elif not hasattr(obj, 'financial'):
                completion_url = reverse_lazy(
                    'order_registration:create_financial',
                    kwargs={
                        'main_data_id': obj.pk
                    }
                )
            elif not obj.ware_set.all():
                completion_url = reverse_lazy(
                    'order_registration:ware_list',
                    kwargs={
                        'main_data_id': obj.pk
                    }
                )
            elif not obj.document:
                completion_url = reverse_lazy(
                    'order_registration:upload_document',
                    kwargs={
                        'pk': obj.pk
                    }
                )
        context["statuses"] = statuses
        context['completion_url'] = completion_url
        return context


class MainDataStatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, main_data_id, operation=None, * args, **kwargs):
        user = self.request.user
        main_data = get_object_or_404(MainData, user=user, pk=main_data_id)
        if not operation:
            next_status = main_data.get_next_status_from_current_status()
        else:
            next_status = 'c'
        if next_status:
            main_data.status = next_status
            if next_status == 'r':
                main_data.registrations_number = generate_random_number(8)
            main_data.save()
        return redirect('order_registration:detail', pk=main_data_id)


class CurrencySupplyJsonListView(View):
    def get(self, request, currency_operation_type=None):
        if currency_operation_type:
            q = CurrencySupply.objects.filter(
                currency_operation_type=currency_operation_type)
        else:
            q = CurrencySupply.objects.all()
        data = list(
            q.values('title', 'id')
        )
        return JsonResponse(data=data, safe=False)


class WareUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ware
    form_class = WareForm
    template_name = "order_registration/partials/update_ware_form.html"
    success_message = 'کالای شما با موفقیت به روز رسانی شد.'

    def get_success_url(self):
        obj = self.object
        return reverse_lazy('order_registration:ware_list', kwargs={'main_data_id': obj.main_data.pk})


class WareBulkDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        try:
            q = Ware.objects.filter(main_data__user=user, pk__in=data)
            q.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.info(str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def generate_order_registration_pdf(request, pk):
    # داده‌های نمونه
    main_data = get_object_or_404(MainData, user=request.user, pk=pk)

    # رندر کردن تمپلیت به HTML
    j_date = JalaliDate.today()
    jalali_now = j_date.strftime("%A, %d %B %Y", locale="fa")
    context = {'main_data': main_data,
               'jalali_now': jalali_now,
               'image_path': 'file://' + str(settings.BASE_DIR / 'static' / 'images' / 'logo.png')
               }

    # return render(request, 'order_registration/pdf.html', context)
    html_string = render_to_string(
        'order_registration/pdf.html', context)

    # تنظیمات فونت برای پشتیبانی از زبان فارسی
    font_config = FontConfiguration()
    html = HTML(string=html_string)
    pdf = html.write_pdf(font_config=font_config)

    # ایجاد پاسخ HTTP با نوع محتوای PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    return response


class PayView(LoginRequiredMixin, View):
    def post(self, request):
        session_key = request.session.session_key
        if not session_key:
            # اگر session_key وجود ندارد، یک session جدید ایجاد می‌کنیم
            request.session.create()
            session_key = request.session.session_key
        request.session['main_data_id'] = request.POST.get('main_data_id')
        request.session.modified = True
        return redirect('payments:payments')
