from django.http import HttpResponse, JsonResponse
from core_app.models import Incident, Image, User
from django.shortcuts import render, redirect, get_object_or_404
import time
import sys
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import core_app.utils.auto_send_email as auto_send_email

sys.path.append('core_app/utils')


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

def index(request):
    return HttpResponse("Report Success!")


def home(request):
    return render(request, "core_app/Home.html")

def report(request):
    return render(request, "core_app/Report.html")

def showIncident(request):
    return render(request, "core_app/Incident.html")


def user_login(request):
    if request.method == "POST":
        name = request.POST.get("uname", None)
        psw = request.POST.get("psw", None)

    return render(request, "core_app/Login.html")


receivers = ['dardat@tcd.ie', 'habeebra@tcd.ie', 'pedgaoks@tcd.ie', 'wangx33@tcd.ie', 'zhangj20@tcd.ie', 'welin@tcd.ie']


def report_incident(request):
    if request.method == "POST":
        id = None
        location = request.POST.get("location", None)
        description = request.POST.get("description", None)
        image_list = request.FILES.getlist('images')
        image = None
        for img in image_list:
            image = img

        incident_type = request.POST.get("category", None)
        occur_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        status = "active"
        traffic_status = "crowded"
        scale_impact = request.POST.get("impactScale", None)
        incident = Incident(id=id, location=location,description=description, images=image, incident_type=incident_type,
                            occur_time=occur_time,
                            status=status,traffic_status=traffic_status,scale_impact=scale_impact)
        incident.save()
        # for image in image_list:
        #     img_instance = Image(image=image)
        #     img_instance.save()
        #     incident.images.add(img_instance)
        print(image)
        auto_send_email.send_email(f"\nLocation: {location} \nIncident-type:{incident_type} \nDescription: {description} \nStatus: {status}", receivers)
    return render(request, "core_app/Report.html")
    #return redirect("core_app:getIncident")
    # response_data = {'success': True, 'message': 'Report Success！'}
    # return JsonResponse(response_data)



def getIncident(request):
    incidents = Incident.objects.all()
    for incident in incidents:
        print(f"{incident.images.url}")
    return render(request, 'core_app/Incident.html', {'incidents': incidents})


def getUsers():
    users = User.objects.all()
    return users
