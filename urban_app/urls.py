"""
URL configuration for urban_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path

from core_app import views
from urban_app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', views.index, name="index"),
    # path('report_incident/', views.report_incident, name='report_incident'),
    # path('home/', views.home, name='home'),
    # path('report/', views.report, name='report'),
    path("login", views.user_login, name="user_login"),
    path('core_app/', include(('core_app.urls', 'core_app'), namespace='core_app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
