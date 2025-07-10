from django.db import models

class Incident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    user_ip = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True)
    lat_location = models.CharField(max_length=255, null=True)
    long_location = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    images = models.ImageField(upload_to='incident_images/', blank=True, null=True)
    incident_type = models.CharField(max_length=255, null=True)
    occur_time = models.DateTimeField()
    status = models.CharField(max_length=255, null=True)
    traffic_status = models.CharField(max_length=255, null=True)
    scale_impact = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'incident'
        
class Image(models.Model):
    incident = models.ForeignKey(Incident, related_name='incident_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='incident_images/', blank=True, null=True)
    class Meta:
        db_table = 'image'

class User(models.Model):
    report_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    user_ip = models.CharField(max_length=255, null=True)
    incident_id = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'user'

class Weather(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255, null=True)
    sub_location = models.CharField(max_length=255, null=True)
    disaster_status = models.CharField(max_length=255, null=True)
    predicted_disaster_status = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'weather'
