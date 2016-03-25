# xoxzo api libirary
"""
This is the API library for Xoxzo's telephony service.
"""

import requests
import os

__author__ = "Akira Nonaka <nonaka@mac.com>"
__status__ = "development"
__version__ = "0.1"
__date__ = "25 March 2011"


class XoxzoClient:

    def __init__(self, sid=None, auth_token=None):
        api_host = os.environ.get("XOXZO_API_HOST")
        if api_host is not None:
            xoxzo_api_host = api_host
        else:
            xoxzo_api_host = "https://api.xoxzo.com"

        self.xoxzo_api_sms_url = xoxzo_api_host + "/sms/messages/"
        self.xoxzo_api_voice_simple_url = (
            xoxzo_api_host + "/voice/simple/playback/")

        if sid is None:
            self.sid = os.environ.get("XOXZO_API_SID")
        else:
            self.sid = sid

        if auth_token is None:
            self.auth_token = os.environ.get("XOXZO_API_AUTH_TOKEN")
        else:
            self.auth_token = auth_token

        self.send_sms_last_response = None
        self.voice_palyback_last_response = None

    def send_sms(self, message, recipient, sender):
        payload = {
            'message': message,
            'recipient': recipient,
            'sender': sender}
        self.send_sms_last_response = requests.post(
            self.xoxzo_api_sms_url,
            data=payload,
            auth=(self.sid, self.auth_token))
        # remember the last response for future use
        return self.send_sms_last_response

    def get_sms_delivery_status(self, msgid=None):
        if msgid is None:
            msgid = self.send_sms_last_response.json()[0]['msgid']
        url = self.xoxzo_api_sms_url + msgid
        r = requests.post(url, auth=(self.sid, self.auth_token))
        return r

    def voice_simple_playback(self, caller, recipient, recording_url):
        payload = {
            'caller': caller,
            'recipient': recipient,
            'recording_url': recording_url}
        self.voice_palyback_last_response = requests.post(
            self.xoxzo_api_voice_simple_url,
            data=payload,
            auth=(self.sid, self.auth_token))
        # remember the last response for future use
        return self.voice_palyback_last_response

    def get_voice_simple_playback_status(self, callid=None):
        if callid is None:
            callid = self.voice_palyback_last_response.json()[0]['callid']
        url = self.xoxzo_api_voice_simple_url + callid
        r = requests.post(url, auth=(self.sid, self.auth_token))
        return r
