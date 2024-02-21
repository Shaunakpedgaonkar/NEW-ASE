# models.py
from django.db import models


class Incident(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    images = models.ImageField(upload_to='incident_images/', blank=True, null=True)
    incident_type = models.CharField(max_length=255, null=True)
    occur_time = models.DateTimeField()
    status = models.CharField(max_length=255, null=True)
    traffic_status = models.CharField(max_length=255, null=True)
    scale_impact = models.CharField(max_length=255, null=True)
    #lat_lng = models.CharField(max_length=255, null=True)
    extrainfo = models.JSONField()
    class Meta:
        db_table = 'incident'


class User(models.Model):
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'user'


class Image(models.Model):
    image = models.ImageField(upload_to='incident_images/', blank=True, null=True)
    class Meta:
        db_table = 'image'
