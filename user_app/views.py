import time
import sys
import math
import json
from datetime import datetime
from django.utils.timezone import make_aware
from .models import Incident, User, Weather
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail

@method_decorator(csrf_exempt, name='dispatch')
class editStatusView(View):
    def post(self, request, incident_id):
        try:
            new_status = request.POST.get('status')
            incident = Incident.objects.get(pk=incident_id)
            incident.status = new_status
            incident.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)})

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in meters between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000
    return c * r



def home_user(request):
    incidents = Incident.objects.filter(status='active').values('lat_location', 'long_location', 'incident_type')
    incidents_list = list(incidents)
    incidents_json = json.dumps(incidents_list)
    latest_incidents = Incident.objects.filter(status='active').order_by('-occur_time')[:3]
    # Fetch disaster data using the disaster detection system
    disaster_results = Weather.objects.all()

    return render(request, "user/Home_User.html", {'recent_incidents': latest_incidents,'incidents_json': incidents_json,'disaster_detections' : disaster_results})


def report_user(request):
    if request.method == "POST":
        id = None
        username = request.POST.get("username", None)
        location = request.POST.get("location", None)
        lat  = request.POST.get("latitude", None)
        long = request.POST.get("longitude", None)
        description = request.POST.get("description", None)
        image_list = request.FILES.getlist('images')
        image = None
        for img in image_list:
            image = img

        incident_type = request.POST.get("category", None)
        occur_time = make_aware(datetime.now())
        status = "active"
        traffic_status = request.POST.get("trafficStatus", None)
        scale_impact = request.POST.get("impactScale", None)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            similar_incident_found = False
        for incident in Incident.objects.filter(incident_type=incident_type, occur_time__date=occur_time.date()):
            incident_lat = float(incident.lat_location)
            incident_long = float(incident.long_location)
            print(long, lat, incident_long, incident_lat)
            distance = haversine(float(long), float(lat), incident_long, incident_lat)
            if distance <= 500:
                similar_incident_found = True
                user = User.objects.create(report_id =None,username=username,user_ip=ip, incident_id=incident.incident_id)
                return render(request, "user/Report_User.html")
        if similar_incident_found == False:
            incident = Incident.objects.create(incident_id=id,user_name=username, user_ip=ip, location=location,lat_location = lat ,long_location = long ,description=description, images=image, incident_type=incident_type,
                            occur_time=occur_time,
                            status=status,traffic_status=traffic_status,scale_impact=scale_impact)
            id = incident.incident_id
            user = User.objects.create(report_id =None,username=username,user_ip=ip, incident_id=id)
            subject = 'New Incident Report'
            message = f"""
            Location: {location}
            Incident-type: {incident_type}
            Description: {description}
            Status: {status}
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    'ghostprotocal010@gmail.com',
                    receivers,
                    fail_silently=False,
                )
                return redirect('user:getIncidentUser')
            except Exception as e:
                return HttpResponse(f"Error in sending email: {e}")
        else:
            return redirect('user:getIncidentUser')
    return render(request, "user/Report_User.html")

receivers = ['dardat@tcd.ie', 'habeebra@tcd.ie', 'pedgaoks@tcd.ie']

def getIncidentUser(request):
    incidents = Incident.objects.all()
    for incident in incidents:
        for incident in incidents:
            if not incident.images:
                incident.image_url = None
            else:
                incident.image_url = incident.images.url
    return render(request, 'user/Incident_User.html', {'incidents': incidents})

def getUsers():
    users = User.objects.all()
    return users

def help_user(request):
    return render(request, 'user/Help_user.html')

def resources_user(request):
    return render(request, 'user/Resources_User.html')
