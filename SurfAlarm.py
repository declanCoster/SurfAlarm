from datetime import datetime, timedelta
from threading import Timer
import requests
import json
import webbrowser
from pprint import pprint
import arrow
from config import TELEGRAM_SEND_MESSAGE_URL
import time 


'''
Note: When testing be aware of the break statements that are placed in the section of checkSurf which accounts for what the conditions are like.
If anything is changed, make sure to comment next to it, because it will make checking the code much easier
'''

going = True

def checkSurf():
        start = arrow.utcnow()
        end = arrow.utcnow().shift(hours= +0)
        #'''
        response = requests.get(
            "https://api.stormglass.io/v2/weather/point",
            params = {
                'lat' :  39, # change for 
                'lng' : -74, # Change for your location
                'params' : ','.join(['waveHeight', 'windDirection', 'windSpeed', 'wavePeriod']),
                'start' : start,
                'end' : end
            },
            headers = { 
                "Authorization" : "" #stormglass authorization
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
               if aveDict.get(ele) <= .5: #this is a check for height
                   alarm = False
                   break
               message = message + "Wave Height : " + str(aveDict.get(ele)*3.28084) + "ft\n"
           if ele == 'windDirection':
                if aveDict.get(ele) < 190 and aveDict.get(ele) > 10: #this is a check for off shore wind
                   alarm = False
                   break 
                message = message + "Wind Direction : " + str(aveDict.get(ele)) + "degrees\n"
           if ele == 'windSpeed':
                message = message + "Wind Speed : " + str(aveDict.get(ele)*2.23694) + "mph\n" 
           if ele == 'windPeriod':
                message = message + "Wave Period : " + str(aveDict.get(ele)) + "seconds\n" 
        alarm = True # this is only for test    
        if alarm:      
           requests.get(TELEGRAM_SEND_MESSAGE_URL.format( -423921262 , message)) 

going = True

while going:
    x = datetime.today().hour
    wait = 0
    if x != 5: #should be 5 for 5am
        wait = 300
    else:
        checkSurf()
        wait = 85500
    time.sleep(wait)
