from django.db import models
import datetime as dt

class Houmer(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class HoumerLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    houmerId = models.ForeignKey(Houmer, on_delete=models.CASCADE, related_name='locations')
    deviceId = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)


class Property(models.Model):
    visited_by = models.ForeignKey(Houmer, on_delete=models.CASCADE, related_name='properties_visited')
    arrive_at = models.DateTimeField(auto_now=True)
    departure_at = models.DateTimeField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    @property
    def elapsed_time_ms(self):
        elapsed_time = self.departure_at - self.arrive_at
        return int(elapsed_time.total_seconds() * 1000)
    
    @property
    def elapsed_time_str(self):
        elapsed_time = self.departure_at - self.arrive_at
        return dt.timedelta(seconds=elapsed_time.total_seconds())
