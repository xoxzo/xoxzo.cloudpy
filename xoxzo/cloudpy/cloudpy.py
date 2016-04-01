# xoxzo api libirary

'''
This is the API library for Xoxzo's telephony service.
http://docs.xoxzo.com/en/

see http://docs.python-requests.org/en/master/ for requests library.
'''

import requests
import os

__author__ = "Akira Nonaka <nonaka@mac.com>"
__status__ = "development"
__version__ = "0.1"
__date__ = "30 March 2011"


class XoxzoClient:
    '''
    Base class to access Xoxzo API.

    :param string sid:  Your sid of the xoxzo account.
    :param string auth_token: Your auth_token of the xoxzo account.
    '''

    def __init__(self, sid, auth_token):
        '''
        Initialize and instanceate XoxzoClient object.
        '''
        self.sid = sid
        self.auth_token = auth_token
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

    def send_sms(self, message, recipient, sender):
        '''
        Send sms to the recipient.

        :param string message: Message body.
        :param string recipient: Message recipient.
        :param string sender: Sender ID.
        :return: list of message id when success,
            dict of error reason when fail.
        :rtype: dict or list.
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
        Get sms delivery status.

        :param string msgid: msgid of the return valun of send_sms() method.
        :return: sms send status information.
        :rtype: dict.
        '''

        url = self.xoxzo_api_sms_url + msgid
        response = requests.get(url, auth=(self.sid, self.auth_token))
        return response.json()

    def call_simple_playback(self, caller, recipient, recording_url):
        '''
        Make a phone call and playback MP3 sound file.

        :param string caller: caller phone number.
        :param string recipient: Phone call recipient.
        :param string recording_url: MP3 file URL.
        :return: list of call id when success,
            dict of error reason when fail.
        :rtype: dict or list.
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
        Get simple palyback status.

        :param string callid: callid of the return valun of
            call_simple_playback() method.
        :return: call playback status information.
        :rtype: dict.
        '''

        url = self.xoxzo_api_voice_simple_url + callid
        response = requests.get(url, auth=(self.sid, self.auth_token))
        return response.json()
