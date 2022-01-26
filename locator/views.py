from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HoumerLocationSerializer
from .models import HoumerLocation


class HoumerLocationViewSet(APIView):
    def post(self, request, format=None):
        validator = HoumerLocationSerializer(data=request.data)
        validator.is_valid(raise_exception=True)
        validator.save()
        return Response(data=validator.data, status=status.HTTP_201_CREATED)
