from rest_framework import serializers
from django.utils import timezone

from .models import HoumerLocation, Property

class HoumerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoumerLocation
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    elapsed_time_ms = serializers.IntegerField(read_only=True)
    elapsed_time_str = serializers.CharField(read_only=True)

    def validate_departure_at(self, value):
        now = timezone.now()
        if value <= now:
            raise serializers.ValidationError('Departure datetime is less than arrive time')
        return value

    class Meta:
        model = Property
        fields = ('visited_by', 'arrive_at', 'departure_at', 'latitude', 'longitude', 'elapsed_time_ms', 'elapsed_time_str')
