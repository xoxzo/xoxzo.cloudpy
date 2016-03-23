# xoxzo api libirary

import requests
import json

class XoxzoCloud:
    def __init__(self,sid,auth_token):
        self.sid = sid
        self.auth_token = auth_token

    def send_sms(self,message,recipient,sender):
        url = "https://api.xoxzo.com/sms/messages/"
        payload = {'message' : message,
              'recipient' : recipient,
              'sender' : sender }
        r = requests.post(url, data=payload,auth=(self.sid,self.auth_token))
        return r

    def get_delivery_status(self,msgid):
        url = "https://api.xoxzo.com/sms/messages/" + msgid
