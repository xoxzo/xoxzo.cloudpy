# xoxzo api libirary

import requests
import json


class XoxzoCloud:
    def __init__(self, sid, auth_token):
        self.sid = sid
        self.auth_token = auth_token
        self.send_sms_last_respose = None
        self.voice_palyback_last_respose = None

    def send_sms(self, message, recipient, sender):
        url = "https://api.xoxzo.com/sms/messages/"
        payload = {
            'message': message,
            'recipient': recipient,
            'sender': sender}
        self.send_sms_last_respose = requests.post(
            url,
            data=payload,
            auth=(self.sid, self.auth_token))
        # remember the last response for future use
        return self.send_sms_last_respose

    def get_sms_delivery_status(self, msgid):
        url = "https://api.xoxzo.com/sms/messages/" + msgid
        r = requests.post(url, auth=(self.sid, self.auth_token))
        return r

    def voice_playback(self, caller, recipient, recording_url):
        url = "https://api.xoxzo.com/voice/simple/playback/"
        payload = {
            'caller': caller,
            'recipient': recipient,
            'recording_url': recording_url}
        self.voice_palyback_last_respose = requests.post(
            url,
            data=payload,
            auth=(self.sid, self.auth_token))
        # remember the last response for future use
        return self.voice_palyback_last_respose

    def get_voice_playback_status(self, callid):
        url = "https://api.xoxzo.com/voice/simple/playback/" + callid
        r = requests.post(url, auth=(self.sid, self.auth_token))
        return r
