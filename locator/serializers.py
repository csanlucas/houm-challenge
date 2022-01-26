from rest_framework import serializers

from .models import HoumerLocation

class HoumerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoumerLocation
        fields = '__all__'
