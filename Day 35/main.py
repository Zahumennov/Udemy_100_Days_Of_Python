# import requests
#
# WEATHER_API_KEY = ''
# MY_LAT = 42.497681
# MY_LONG = 27.470030
#
# # parameters = {
# #     'appid': WEATHER_API_KEY,
# #     'lat': MY_LAT,
# #     'lon': MY_LONG
# # }
# # response = requests.get('https://api.openweathermap.org/data/3.0/onecall', params=parameters)
#
# parameters = {
#     'appid': WEATHER_API_KEY,
#     'q': 'Burgas',
# }
# response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters)
# response.raise_for_status()
# weather_data = response.json()
#
#
#Note! For the code to work you need to replace all the placeholders with
#Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": os.environ.get("LATITUDE"),
    "lon": os.environ.get("LONGITUDE"),
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=os.environ.get("TWILIO_VIRTUAL_NUMBER"),
        to=os.environ.get("TWILIO_VERIFIED_REAL_NUMBER")
    )
    print(message.status)
