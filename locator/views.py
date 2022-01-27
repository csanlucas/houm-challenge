from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
import datetime as dt
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .serializers import HoumerLocationSerializer, PropertySerializer
from .models import HoumerLocation, Houmer, Property
from .pagination import PaginationHandlerMixin


class HoumerLocationViewSet(APIView, PaginationHandlerMixin):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self, request):
        if all(k in request.query_params for k in ("houmer_id", "on_date", "velocity_kmh")):
            try:
                velocity_kmh = int(request.query_params['velocity_kmh'])
            except ValueError:
                return Response({'message': 'Provide a valid integer query_params [velocity_kmh]'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                query_date = dt.datetime.fromisoformat(request.query_params['on_date'])
                query_date = timezone.get_current_timezone().localize(query_date)
            except ValueError:
                return Response({'message': 'Check on date params must be in format YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
            houmer = get_object_or_404(Houmer, pk=request.query_params['houmer_id'])
            locations_filtered = houmer.locations.filter(created_at__gt=query_date,
                created_at__lt=query_date.replace(hour=23, minute=59, second=59), velocity_kmh__gt=request.query_params['velocity_kmh'])
        else:
            locations_filtered = HoumerLocation.objects.all()
        page = self.paginate_queryset(locations_filtered)
        if page is not None:
            serializer = self.get_paginated_response(HoumerLocationSerializer(page, many=True).data)
        else:
            serializer = HoumerLocationSerializer(locations, many=True)
        return Response(data=serializer.data)

    def post(self, request, format=None):
        validator = HoumerLocationSerializer(data=request.data)
        validator.is_valid(raise_exception=True)
        validator.save()
        return Response(data=validator.data, status=status.HTTP_201_CREATED)


class PropertyViewSet(APIView, PaginationHandlerMixin):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

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
        page = self.paginate_queryset(properties_visited)
        if page is not None:
            serializer = self.get_paginated_response(PropertySerializer(page, many=True).data)
        else:
            serializer = PropertySerializer(properties_visited, many=True)
        return Response(data=serializer.data)


    def post(self, request):
        validator = PropertySerializer(data=request.data)
        validator.is_valid(raise_exception=True)
        validator.save()
        return Response(data=validator.data, status=status.HTTP_201_CREATED)
