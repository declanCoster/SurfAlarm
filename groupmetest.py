from datetime import datetime, timedelta
from threading import Timer
import requests
import json
import webbrowser
from pprint import pprint
import arrow
import time

#get the arrow for just this hour
start = arrow.utcnow()
end = arrow.utcnow().shift(hours= +0)

#make the request from the stormglass api
response = requests.get(
    "https://api.stormglass.io/v2/weather/point",
    params = {
                'lat' :  39,
                'lng' : -74,
                'params' : ','.join(['waveHeight', 'windDirection', 'windSpeed', 'wavePeriod']),
                'start' : start,
                'end' : end
            },
    headers = { 
                "Authorization" : "storm key"
            }
        )

#the request
oceanInfo = response.json()
message = 'Bomb Squad Alarm: '
message = message + arrow.now().format('MM/DD/YYYY  HH:mm:ss') + '\n'

#make the dictionary for the elements
aveDict = dict()
for ele in oceanInfo.get('hours')[0]:
    if ele != 'time':
        lis = oceanInfo.get('hours')[0].get(ele).values()
        total = sum(lis)
        times = len(lis)
        average = total / times
        aveDict[ele] = average
        #oceanInfo.get('hours')[0].get(ele).values()

wind_direction = False
wind_speed = False
wave_height = False
massive = False

for ele in aveDict:
    if ele == 'waveHeight':
        num = aveDict.get(ele)*3.28084
        if num >=1.5:
            wave_height = True
        if num >= 6:
            massive = True
        waveheight = "%5.2f" % num
        message = message + "Wave Height\t\t" + waveheight + " ft\n"
    if ele == 'windDirection':
        num = aveDict.get(ele)
        wind = "%5.2f" % num
        if num <= 10 or num >=230:
            wind_direction = True
        message = message + "Wind Direction\t\t" + wind + " degrees\n"
    if ele == 'windSpeed':
        num = aveDict.get(ele)*2.23694
        if num <= 23:
            wind_speed = True
        windspeed = "%5.2f" % num
        message = message + "Wind Speed\t\t" + windspeed + " mph\n" 
    if ele == 'wavePeriod':
        num = aveDict.get(ele)
        waveperiod = "%5.2f" % num
        message = message + "Wave Period\t\t" + waveperiod + " seconds\n" 

message = message + "\n\nhttps://www.surf-forecast.com/breaks/Wooden-Jetties/forecasts/latest/six_day"

if wind_direction:
    message = "nice wind direction\n\n" + message
elif massive:
    message = "it is massive\n\n" + message

data = {
        'bot_id' : 'id',
        'text' : message,
        }

if wind_direction and wind_speed and wave_height:
        requests.post('https://api.groupme.com/v3/bots/post', json=data)
