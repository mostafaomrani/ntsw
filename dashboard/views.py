from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from order_registration.models import MainData
from users.models import Role
from django.urls import reverse_lazy


class BaseRoleView(View):
    def get(self, request, *args, **kwargs):

        user = request.user
        activate = request.GET.get('activate', None)
        if activate:
            role = Role.objects.get(code=activate)
            user.active_role = role
            user.save()
            # ذخیره نقش فعال در سشن
            request.session['active_role_id'] = role.id
            request.session['active_role_code'] = role.code
        else:
            # اگه نقش قبلاً توی سشن بود از همون استفاده کن
            if 'active_role_id' in request.session:
                try:
                    role = Role.objects.get(id=request.session['active_role_id'])
                    user.active_role = role
                except Role.DoesNotExist:
                    pass


        roles = user.roles.all().order_by('id')


        context = {
            'roles': roles,
            'active_role': user.active_role,
        }
        
        print(roles)

        if user.active_role.id == 1:
            return render(request, 'dashboard/base_role_index.html',context)
        elif user.active_role.id == 5:
            context = {
                'roles': roles,
                'active_role': user.active_role,
                'message': 'این ویو مخصوص تاجر است',
            }
            return render(request, 'dashboard/trader_role_index.html', context)
        elif user.active_role.id == 3 or user.active_role.id == 4:
            main_data = MainData.objects.filter(user=user)
            context = {
                'boxes':
                   [
                       {
                           'icon': 'fa-clipboard',
                           'color_class_suffix': 'bs',
                           'count': main_data.count(),
                           'title': 'پرونده‌های ثبت شده',
                           'main_link': reverse_lazy(
                               'order_registration:main_data_list'
                           ),
                           'links': [
                               (
                                   reverse_lazy(
                                       'order_registration:create_main_data'
                                   ),
                                   'ثبت پرونده جدید'
                               ),
                               (
                                   reverse_lazy(
                                       'order_registration:main_data_list'
                                   ),
                                   'مدیریت پرونده‌ها'
                               )
                           ],
                       },
                       {
                           'icon': 'fa-file-text-o',
                           'color_class_suffix': 'kk',
                           'count': main_data.filter(status='r').count(),
                           'title': 'پرونده‌های تایید شده',
                           'main_link': reverse_lazy(
                               'order_registration:main_data_list'
                           ),
                           'links': [
                               (
                                   reverse_lazy(
                                       'order_registration:main_data_list'
                                   ),
                                   'مدیریت پرونده‌ها'
                               ),
                           ],
                       },
                       {
                           'icon': 'fa-list-alt',
                           'color_class_suffix': 'navy',
                           'count': 0,
                           'title': 'گشایش‌های اعتبار اسنادی/ حواله/ برات تایید شده',
                           'main_link': '#',
                           'links': [
                           ],
                           # todo add link
                       },
                       {
                           'icon': 'fa-credit-card',
                           'color_class_suffix': 'ib',
                           'count': 0,
                           'title': 'منشا ارزهای غیربانکی ثبت شده',
                           'main_link': '#',
                           'links': [
                               (
                                   '#',
                                   'مدیریت منشا ارز غیربانکی'

                               )
                           ],
                           #    Todo: add links

                       },
                       {
                           'icon': 'fa-users',
                           'color_class_suffix': 'dp',
                           'count': 0,
                           'title': 'نمایندگان فعال',
                           'main_link': '#',
                           'links': [
                               (
                                   '#',
                                   'مدیریت نمایندگان'
                               )
                               # Todo: add links
                           ],


                       },
                       {
                           'icon': 'fa-money',
                           'color_class_suffix': 'ma',
                           'count': 0,
                           'title': 'منشا ارزهای بانکی ثبت شده',
                           'main_link': '#',
                           'links': [],

                       },

                   ],
                    'roles': roles,
                    'active_role': user.active_role,
                   }
            return render(request, 'dashboard/business_role_index.html', context)