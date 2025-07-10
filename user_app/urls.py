#user_app/urls.py
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home_user', views.home_user, name="home_user"),
    path('report_user/', views.report_user, name='report_user'),
    path('getIncidentUser/', views.getIncidentUser, name='getIncidentUser'),
    path('help_user/', views.help_user, name='help_user'),
    path('resources_user/', views.resources_user, name='resources_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
