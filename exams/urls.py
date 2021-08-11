"""exams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from  django.conf import settings
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

admin.site.site_header = 'Tehnical School'

app_name='exams'


handler400 = 'account.views.bad_request'
handler403 = 'account.views.custom_permissin_denied_view'
handler404 = 'account.views.custom_page_not_found_view'
handler500 = 'account.views.custom_error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("account.urls")),
    path('accounts/', include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

