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
__date__ = "25 March 2011"


class XoxzoClient:
    '''
    root class that access Xoxzo API

    '''
    def __init__(self, sid=None, auth_token=None):
        '''
        initialize and instanceate XoxzoClient object

        sid: your sid of xoxzo account
            if None, value of environment variable XOXZO_API_SID is used.

        auth_token: your auth_token of xoxzo account
            if None, value of environment variable XOXZO_API_AUTH_TOKEN
            is used.
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

        self.send_sms_last_response = None
        self.voice_palyback_last_response = None

    def send_sms(self, message, recipient, sender):
        '''
        send sms to the recipient.

        message: Message body
        recipient: Message recipient
        sender: Sender ID

        return: Response object of the Requests library for Python
        '''
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
        '''
        get sms delivery status.

        msgid: msgid of the return valun of send_sms() method.
            if None, the message id of the last send_sms() method call
            will be used.

        return: Response object of the Requests library for Python

        '''

        if msgid is None:
            res = self.send_sms_last_response.json()
            if isinstance(res, dict):
                # most likely, bad sid,auth_token was used in previouss call
                return self.send_sms_last_response
            '''
            if prevouse send_sms call success, send_sms_last_response is list
            and first element is dict(json) and shoud have key msgid.

            '''
            msgid = res[0]['msgid']

        url = self.xoxzo_api_sms_url + msgid
        r = requests.get(url, auth=(self.sid, self.auth_token))
        return r

    def call_simple_playback(self, caller, recipient, recording_url):
        '''
        make a phone call and play back MP3 sound file.

        caller: caller phone number
        recipient: Phone call recipient.
        recording_url: MP3 file URL
        '''
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

    def get_simple_playback_status(self, callid=None):
        '''
        get simple palyback status.

        callid: msgid of the return valun of send_sms() method.
            if None, the callid id of the last call_simple_playback()
            method call will be used.

        return: Response object of the Requests library for Python
            see http://docs.python-requests.org/en/master/ for details.
        '''

        if callid is None:
            callid = self.voice_palyback_last_response.json()[0]['callid']
        url = self.xoxzo_api_voice_simple_url + callid
        r = requests.get(url, auth=(self.sid, self.auth_token))
        return r
