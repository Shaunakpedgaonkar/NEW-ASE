from django.db import models


class staff(models.Model):
    username = models.CharField(max_length=255, null=True)
    incident = models.CharField(max_length=255, null=True)
    time = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'staff'
        
