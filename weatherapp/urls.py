from django.urls import path
from . import views

urlpatterns = [path("", views.get_weather_data, name="get-weather-data")]
