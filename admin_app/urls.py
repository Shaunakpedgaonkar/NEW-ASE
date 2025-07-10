# admin_app/urls.py
from django.urls import path
from .views import report_incident, home, report, getIncident, editStatusView, staff_login, staff_logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', staff_login, name='staff_login'),
    path('logout/', staff_logout, name='staff_logout'),
    path('home/', home, name='home'),
    path('report/', report, name='report'),
    path('report_incident/', report_incident, name='report_incident'),
    path('getIncident/', getIncident, name='getIncident'),
    path('edit_status/<int:incident_id>/', editStatusView.as_view(), name='edit_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
