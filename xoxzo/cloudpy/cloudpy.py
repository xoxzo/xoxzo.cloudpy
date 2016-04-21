# xoxzo api libirary

'''
This is the API library for Xoxzo's telephony service.
http://docs.xoxzo.com/en/

see http://docs.python-requests.org/en/master/ for requests library.
'''

import requests
import os
import json

__author__ = "Akira Nonaka <nonaka@mac.com>"
__status__ = "development"
__version__ = "0.1"
__date__ = "30 March 2011"


class XoxzoResponse:

    def __init__(self, message={}, messages=[], errors=None):
        """

        :rtype: XoxzoResponse
        """
        self.message = message
        self.messages = messages
        self.errors = errors


class XoxzoClient:
    '''
    Base class to access Xoxzo API.

    :param string sid: Your sid of the xoxzo account.
    :param string auth_token: Your auth_token of the xoxzo account.
    :param string api_host: If None, stadard xoxzo server will be used.
    '''
    REQUESTS_EXCEPITON = 499

    def __init__(self, sid, auth_token, api_host=None):
        '''
        Initialize and instanceate XoxzoClient object.
        '''
        self.sid = sid
        self.auth_token = auth_token

        if api_host is None:
            api_host = "https://api.xoxzo.com"

        self.xoxzo_api_sms_url = api_host + "/sms/messages/"
        self.xoxzo_api_voice_simple_url = (
            api_host + "/voice/simple/playback/")

    def send_sms(self, message, recipient, sender):
        '''
        Send sms to the recipient.

        :param string message: Message body.
        :param string recipient: Message recipient.
        :param string sender: Sender ID.
        :return: if XoxzoResponse.errors == None, list of message ids are returned in XoxzoResponse.messages.
            otherwise, error coed is retruned in XoxzoResponse.errors and detailed error message is set in
            XoxzoResponse.message.
        :rtype: XoxzoResponse
        '''

        try:
            payload = {
                'message': message,
                'recipient': recipient,
                'sender': sender}
            req_res = requests.post(
            self.xoxzo_api_sms_url,
            data=payload,
            auth=(self.sid, self.auth_token))
            if req_res.status_code == 201:
            # when success, return list
                xr = XoxzoResponse(messages=req_res.json())
            else:
                xr = XoxzoResponse(
                        errors=req_res.status_code,
                        message=req_res.json())
        except requests.exceptions.RequestException as e:
            xr =  XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
        finally:
            return xr


    def get_sms_delivery_status(self, msgid):
        '''
        Get sms delivery status.

        :param string msgid: msgid of the return valun of send_sms() method.
        :return: TBD
        :rtype: XoxzoResponse
        '''

        try:
            url = self.xoxzo_api_sms_url + msgid
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
            if req_res.status_code == 200:
                xr = XoxzoResponse(message=req_res.json())
            else:
                xr = XoxzoResponse(
                            errors=req_res.status_code,
                            message=req_res.json())

        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
        finally:
            return xr

    def get_sent_sms_list(self, sent_date=None):
        '''
        Get sent messages list

        :param string sent_date: search condition date string.
            see http://docs.xoxzo.com/en/sms.html#sent-messages-list-api.
        :return: TBD
        :rtype: XoxzoResponse
        '''

        try:
            if sent_date is None:
                url = self.xoxzo_api_sms_url
            else:
                url = self.xoxzo_api_sms_url + '?sent_date' + sent_date

            req_res = requests.get(url, auth=(self.sid, self.auth_token))
            if req_res.status_code == 200:
                xr = XoxzoResponse(messages=req_res.json())
            else:
                xr = XoxzoResponse(
                            errors=req_res.status_code,
                            message=req_res.json())

        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
        finally:
            return xr

    def call_simple_playback(self, caller, recipient, recording_url):
        '''
        Make a phone call and playback MP3 sound file.

        :param string caller: caller phone number.
        :param string recipient: Phone call recipient.
        :param string recording_url: MP3 file URL.
        :return: TBD
        :rtype: XoxzoResponse
        '''

        try:
            payload = {
                'caller': caller,
                'recipient': recipient,
                'recording_url': recording_url}
            req_res = requests.post(
                self.xoxzo_api_voice_simple_url,
                data=payload,
                auth=(self.sid, self.auth_token))
            if req_res.status_code == 201:
                xr = XoxzoResponse(messages=req_res.json())
            else:
                xr = XoxzoResponse(
                            errors=req_res.status_code,
                            message=req_res.json())

        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
        finally:
            return xr

    def get_simple_playback_status(self, callid):
        '''
        Get simple palyback status.

        :param string callid: callid of the return valun of
            call_simple_playback() method.
        :return: TBD
        :rtype: XoxzoResponse.
        '''

        try:
            url = self.xoxzo_api_voice_simple_url + callid
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
            if req_res.status_code == 200:
                xr = XoxzoResponse(message=req_res.json())
            else:
                xr = XoxzoResponse(
                            errors=req_res.status_code,
                            message=req_res.json())

        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
        finally:
            return xr
