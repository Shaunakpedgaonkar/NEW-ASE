from django.contrib import admin
from django.urls import path
from . import views
from .views import editStatusView

app_name = 'core_app'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('report_incident/', views.report_incident, name='report_incident'),
    path('home/', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('getIncident/', views.getIncident, name='getIncident'),
    path('edit_status/<int:incident_id>/', editStatusView.as_view(), name='edit_status'),
]