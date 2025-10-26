from django.shortcuts import render
from django.views import View
from order_registration.models import MainData
from users.models import Role
from django.urls import reverse_lazy
from django.http import HttpResponse


class BaseRoleView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        activate = request.GET.get('activate', None)

        # اگر کاربر نقش فعال انتخاب کرده
        if activate:
            try:
                role = Role.objects.get(code=activate)
                user.active_role = role
                user.save()
                # ذخیره نقش فعال در سشن
                request.session['active_role_id'] = role.id
                request.session['active_role_code'] = role.code
            except Role.DoesNotExist:
                return HttpResponse("نقش انتخاب شده موجود نیست.")

        else:
            # اگر نقش قبلاً توی سشن بود از همون استفاده کن
            role = None
            if 'active_role_id' in request.session:
                try:
                    role = Role.objects.get(id=request.session['active_role_id'])
                except Role.DoesNotExist:
                    pass

            if role:
                user.active_role = role

        # اگر هنوز نقش فعال وجود ندارد، اولین نقش کاربر را به عنوان پیش‌فرض انتخاب کن
        if not user.active_role:
            default_role = user.roles.first()
            if default_role:
                user.active_role = default_role
                request.session['active_role_id'] = default_role.id
                request.session['active_role_code'] = default_role.code
            else:
                return HttpResponse("شما هیچ نقشی ندارید.")

        roles = user.roles.all().order_by('id')

        context = {
            'roles': roles,
            'active_role': user.active_role,
        }

        # نمایش ویو بر اساس نقش فعال
        role_id = user.active_role.id
        if role_id == 1:
            return render(request, 'dashboard/base_role_index.html', context)
        elif role_id == 5:
            context['message'] = 'این ویو مخصوص تاجر است'
            return render(request, 'dashboard/trader_role_index.html', context)
        elif role_id in [3, 4]:
            main_data = MainData.objects.filter(user=user)
            context['boxes'] = [
                {
                    'icon': 'fa-clipboard',
                    'color_class_suffix': 'bs',
                    'count': main_data.count(),
                    'title': 'پرونده‌های ثبت شده',
                    'main_link': reverse_lazy('order_registration:main_data_list'),
                    'links': [
                        (reverse_lazy('order_registration:create_main_data'), 'ثبت پرونده جدید'),
                        (reverse_lazy('order_registration:main_data_list'), 'مدیریت پرونده‌ها'),
                    ],
                },
                {
                    'icon': 'fa-file-text-o',
                    'color_class_suffix': 'kk',
                    'count': main_data.filter(status='r').count(),
                    'title': 'پرونده‌های تایید شده',
                    'main_link': reverse_lazy('order_registration:main_data_list'),
                    'links': [
                        (reverse_lazy('order_registration:main_data_list'), 'مدیریت پرونده‌ها'),
                    ],
                },
                {
                    'icon': 'fa-list-alt',
                    'color_class_suffix': 'navy',
                    'count': 0,
                    'title': 'گشایش‌های اعتبار اسنادی/ حواله/ برات تایید شده',
                    'main_link': '#',
                    'links': [],
                },
                {
                    'icon': 'fa-credit-card',
                    'color_class_suffix': 'ib',
                    'count': 0,
                    'title': 'منشا ارزهای غیربانکی ثبت شده',
                    'main_link': '#',
                    'links': [('#', 'مدیریت منشا ارز غیربانکی')],
                },
                {
                    'icon': 'fa-users',
                    'color_class_suffix': 'dp',
                    'count': 0,
                    'title': 'نمایندگان فعال',
                    'main_link': '#',
                    'links': [('#', 'مدیریت نمایندگان')],
                },
                {
                    'icon': 'fa-money',
                    'color_class_suffix': 'ma',
                    'count': 0,
                    'title': 'منشا ارزهای بانکی ثبت شده',
                    'main_link': '#',
                    'links': [],
                },
            ]
            return render(request, 'dashboard/business_role_index.html', context)
        else:
            return HttpResponse("نقش فعال شما تعریف نشده است.")
