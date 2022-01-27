from django.urls import path

from .views import HoumerLocationViewSet, PropertyViewSet

url_locator = [
    path('locator/houmer/', HoumerLocationViewSet.as_view()),
    path('locator/property/', PropertyViewSet.as_view())
]
