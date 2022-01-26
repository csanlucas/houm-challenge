from django.db import models

class HoumerLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    houmerId = models.CharField(max_length=50)
    deviceId = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

