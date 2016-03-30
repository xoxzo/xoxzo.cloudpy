# xoxzo api libirary
"""
This is the API library for Xoxzo's telephony service.
http://docs.xoxzo.com/en/

see http://docs.python-requests.org/en/master/ for requests library.
"""

import requests
import os

__author__ = "Akira Nonaka <nonaka@mac.com>"
__status__ = "development"
__version__ = "0.1"
__date__ = "30 March 2011"


class XoxzoClient:
    '''
    Base class to access Xoxzo API

    :param string sid:  your sid of xoxzo account
        if None, value of environment variable XOXZO_API_SID is used.

    :param string auth_token: your auth_token of xoxzo account
        if None, value of environment variable XOXZO_API_AUTH_TOKEN
        is used.

    '''
    def __init__(self, sid=None, auth_token=None):
        '''
        initialize and instanceate XoxzoClient object
        '''

        # you can override api host by setting envrionment
        # variable XOXZO_API_HOST
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

    def send_sms(self, message, recipient, sender):
        '''
        send sms to the recipient.

        :param string message: Message body
        :param string recipient: Message recipient
        :param string sender: Sender ID
        '''
        payload = {
            'message': message,
            'recipient': recipient,
            'sender': sender}
        response = requests.post(
            self.xoxzo_api_sms_url,
            data=payload,
            auth=(self.sid, self.auth_token))
        return response.json()

    def get_sms_delivery_status(self, msgid):
        '''
        get sms delivery status.

        :param string msgid: msgid of the return valun of send_sms() method.
        '''
        url = self.xoxzo_api_sms_url + msgid
        response = requests.get(url, auth=(self.sid, self.auth_token))
        return response.json()

    def call_simple_playback(self, caller, recipient, recording_url):
        '''
        make a phone call and play back MP3 sound file.

        :param string caller: caller phone number
        :param string recipient: Phone call recipient.
        :param string recording_url: MP3 file URL
        '''
        payload = {
            'caller': caller,
            'recipient': recipient,
            'recording_url': recording_url}
        response = requests.post(
            self.xoxzo_api_voice_simple_url,
            data=payload,
            auth=(self.sid, self.auth_token))
        return response.json()

    def get_simple_playback_status(self, callid):
        '''
        get simple palyback status.

        :param string callid: callid of the return valun of
            call_simple_playback() method.
        '''

        url = self.xoxzo_api_voice_simple_url + callid
        response = requests.get(url, auth=(self.sid, self.auth_token))
        return response.json()
