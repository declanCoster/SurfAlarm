from datetime import datetime, timedelta
from threading import Timer
import requests
import json
import webbrowser
from pprint import pprint
import arrow

#testing boy

TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format('large string') # the large string is the bmsqbot token

TELEGRAM_SEND_MESSAGE_URL = TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'

import time 

start = arrow.utcnow()
end = arrow.utcnow().shift(hours= +0)
        #'''
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
                "Authorization" : ""
            }
        )



oceanInfo = response.json()
message = 'Bomb Squad Alarm: '
message = message + arrow.now().format('MM/DD/YYYY  HH:mm:ss') + '\n'

aveDict = dict()

for ele in oceanInfo.get('hours')[0]:
    if ele != 'time':
        lis = oceanInfo.get('hours')[0].get(ele).values()
        total = sum(lis)
        times = len(lis)
        average = total / times
        aveDict[ele] = average
        
            #oceanInfo.get('hours')[0].get(ele).values()
alarm = True

for ele in aveDict:
    if ele == 'waveHeight':
        message = message + "Wave Height : " + str(aveDict.get(ele)*3.28084) + "ft\n"
    if ele == 'windDirection':
        message = message + "Wind Direction : " + str(aveDict.get(ele)) + "degrees\n"
    if ele == 'windSpeed':
        message = message + "Wind Speed : " + str(aveDict.get(ele)*2.23694) + "mph\n" 
    if ele == 'wavePeriod':
        message = message + "Wave Period : " + str(aveDict.get(ele)) + "seconds\n" 
            
if alarm:      
    requests.get(TELEGRAM_SEND_MESSAGE_URL.format( 'int chat ID' , message)) 
