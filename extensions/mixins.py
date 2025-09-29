from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages


class FilterMixin:
    model = None
    filter_field = None

    def get_filtered_data(self, filter_value):
        if not self.model or not self.filter_field:
            raise ValueError('مدل و فیلد filter_field الزامی است.')

        queryset = self.model.objects.filter(
            **{self.filter_field: filter_value}).values('id', 'title')
        return list(queryset)

    def get_json_response(self, data):
        return JsonResponse(data=data, safe=False)

    def get_filtered_data_by_list(self, filter_list):
        if not self.model or not isinstance(filter_list, list):
            raise ValueError('لیست و مدل اجباری می‌باشد')
        query = Q()
        for field, value in filter_list:
            query &= Q(**{field: value})
        q = self.model.objects.filter(query).values('id', 'title')
        return list(q)


class UpdateStatusMixin:
    model = None
    status_choices = None
    success_message = 'وضعیت با موفقیت به روز رسانی شد.'

    def post(self, request, pk):
        status = request.POST.get('status')
        q = self.model.objects.filter(
            user=request.user, pk=pk)
        if status in self.status_choices and q.exists():
            q.update(status=status)
            obj = q.first()
            messages.success(request, self.success_message)
            return redirect(obj.get_absolute_url())
        return redirect('dashboard:base_role_dashboard')
