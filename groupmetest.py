
import requests

data = {
        'bot_id' : 'bot id',
        'text' : "Wavestorms are for kooks",
        }

requests.post('https://api.groupme.com/v3/bots/post', json=data)