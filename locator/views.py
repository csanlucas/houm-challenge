from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
import datetime as dt
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .serializers import HoumerLocationSerializer, PropertySerializer
from .models import HoumerLocation, Houmer, Property


class HoumerLocationViewSet(APIView):
    def post(self, request, format=None):
        validator = HoumerLocationSerializer(data=request.data)
        validator.is_valid(raise_exception=True)
        validator.save()
        return Response(data=validator.data, status=status.HTTP_201_CREATED)


class PropertyViewSet(APIView):
    def get(self, request):
        if 'houmer_id' not in request.query_params:
            return Response({'message': 'Provide query_params [houmer_id] query params'}, status=status.HTTP_400_BAD_REQUEST)
        if 'on_date' not in request.query_params:
            return Response({'message': 'Provide query_params [on_date] to query property metrics'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            query_date = dt.datetime.fromisoformat(request.query_params['on_date'])
            query_date = timezone.get_current_timezone().localize(query_date)
        except ValueError:
            return Response({'message': 'Check on date params must be in format YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        houmer = get_object_or_404(Houmer, pk=request.query_params['houmer_id'])
        properties_visited = houmer.properties_visited.filter(arrive_at__gt=query_date,
                                                              departure_at__lt=query_date.replace(hour=23, minute=59, second=59))
        prop_serializer = PropertySerializer(instance=properties_visited, many=True) 
        return Response(data=prop_serializer.data)


    def post(self, request):
        validator = PropertySerializer(data=request.data)
        validator.is_valid(raise_exception=True)
        validator.save()
        return Response(data=validator.data, status=status.HTTP_201_CREATED)
