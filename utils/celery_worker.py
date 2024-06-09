import os
from celery import Celery
from dotenv import load_dotenv
import requests
import csv
from settings import celery_settings, settings



celery = Celery(__name__)
celery.conf.broker_url = celery_settings.CELERY_BROKER_URL
celery.conf.result_backend = celery_settings.CELERY_RESULT_BACKEND


@celery.task(name="weather_forcast")
def weather_forcast(days=14,city="sari"):
    WHEATHER_API_URL  = f"http://api.weatherapi.com/v1/forecast.json?key={settings.WHEATHER_API_KEY}&q={city}&days={str(days)}"
    json_response = requests.get(WHEATHER_API_URL).json()

    forcats_list  = json_response.get("forecast").get('forecastday')
    location_dict = json_response.get("location")
    keys          = list(location_dict.keys()) + list(forcats_list[0].keys())
    with open("forcast.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for d in forcats_list:
            writer.writerow(location_dict | d)
            
    
