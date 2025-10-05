"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings

from django.views.generic.base import RedirectView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('upload-qualification/', include('upload_qualifications.urls')),
    path('supplier/', include('overseas_supplier.urls')),
    path('order-registration/', include('order_registration.urls')),
    path('currency-allocation/', include('currency_allocation.urls')),
    path('currency-origin-determining/', include('currency_origin_determining.urls')),
    path('payments/', include('apps.payments.urls')),
    # path('product_identifier/', include('product_identifier.urls')),
    path('shenase/', include('shenase.urls')),
    path('foreintrade/', include('foreintrade.urls')),
    path('production_operations/', include('production_operations.urls')),
    path('anbar/', include('anbar.urls')),
]

# redirect from home to login
urlpatterns += [
    path(
        "",
        RedirectView.as_view(url=reverse_lazy('users:login')),
        name="home",
    ),
]

# zarinpall verification file
urlpatterns += [
    path('35330774.txt', lambda r: HttpResponse(
        '', content_type='text/plain'), name="zarinpal")

]


if settings.IS_DEVELOPMENT_ENVIRONMENT:
    from django.conf import settings
    from django.conf.urls.static import static
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
