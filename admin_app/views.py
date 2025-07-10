from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from user_app.models import Incident,Weather
from django.core.mail import send_mail
import time
import json


receivers = ['dardat@tcd.ie', 'habeebra@tcd.ie', 'pedgaoks@tcd.ie']

def staff_login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('staff:home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'admin/Login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'admin/Login.html')

@login_required
def home(request):
    incidents = Incident.objects.filter(status='active').values('lat_location', 'long_location', 'incident_type')
    incidents_list = list(incidents)
    incidents_json = json.dumps(incidents_list)
    latest_incidents = Incident.objects.filter(status='active').order_by('-occur_time')[:3]
    # Fetch disaster data using the disaster detection system
    disaster_results = Weather.objects.all()

    return render(request, "admin/Home.html", {'recent_incidents': latest_incidents,'incidents_json': incidents_json,'disaster_detections' : disaster_results})

@login_required
def report(request):
    return render(request, "admin/Report.html")

@login_required
def showIncident(request):
    return render(request, "admin/Incident.html")

@login_required
def report_incident(request):
    if request.method == "POST":
        description = request.POST.get("description", None)
        image_list = request.FILES.getlist('images')
        image = image_list[0] if image_list else None  # Assuming only the first image is used

        incident_type = request.POST.get("category", None)
        occur_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        status = "active"

        incident = Incident(
            description=description, 
            images=image, 
            incident_type=incident_type,
            occur_time=occur_time,
            status=status,
        )
        incident.save()

        subject = 'New Incident Report'
        message = f"""
        Location: {incident.location}
        Incident-type: {incident_type}
        Description: {description}
        Status: {status}
        """

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                receivers,
                fail_silently=False,
            )
            return redirect('staff:getIncident')
        except Exception as e:
            return HttpResponse(f"Error in sending email: {e}")
    return render(request, "admin/Report.html")

@login_required
def getIncident(request):
    incidents = Incident.objects.all()
    for incident in incidents:
        for incident in incidents:
            if not incident.images:
                incident.image_url = None
            else:
                incident.image_url = incident.images.url
    return render(request, 'admin/Incident.html', {'incidents': incidents})

def staff_logout(request):
    logout(request)
    return redirect('staff:staff_login')

@method_decorator(login_required, name='dispatch')
class editStatusView(View):
    def post(self, request, incident_id):
        try:
            new_status = request.POST.get('status')
            incident = get_object_or_404(Incident, pk=incident_id)
            incident.status = new_status
            incident.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})
