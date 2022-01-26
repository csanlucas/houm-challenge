from django.urls import path

from .views import HoumerLocationViewSet

url_locator = [
    path('locator/houmer/', HoumerLocationViewSet.as_view())
]
