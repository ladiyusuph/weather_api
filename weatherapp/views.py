from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from datetime import datetime
from django.conf import settings
from django.core.cache import cache


@api_view(["GET"])
def get_weather_data(request):
    location = request.GET.get("location")
    if not location:
        return Response(
            {"Message": "Location is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    date1 = request.GET.get("date1", None)
    date2 = request.GET.get("date2", None)

    if date1 and date2:
        cache_key = f"weather-{date1}-{date2}-{location}"
        weather_data = cache.get(cache_key)
        if not weather_data:
            try:
                weather_data = requests.get(
                    f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date1}/{date2}?key={settings.API_KEY}"
                )
                weather_data = weather_data.json()
                cache.set(cache_key, weather_data, timeout=60 * 60)  # cache for 1 hour
            except requests.exceptions.RequestException as e:
                return Response(
                    {"Message": "Error fetching weather data"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
    else:
        cache_key = f"weather-current-{location}"
        weather_data = cache.get(cache_key)
        if not weather_data:
            try:
                current_date = datetime.now().strftime("%Y-%m-%d")
                weather_data = requests.get(
                    f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{current_date}?key={settings.API_KEY}&include=current"
                )
                weather_data = weather_data.json()
                cache.set(cache_key, weather_data, timeout=60 * 60)  # cache for 1 hour
            except requests.exceptions.RequestException as e:
                return Response(
                    {"Message": "Error fetching weather data"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    return Response(weather_data)
