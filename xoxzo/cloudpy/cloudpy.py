# xoxzo api libirary

'''
This is the API library for Xoxzo's telephony service.
http://docs.xoxzo.com/en/

see http://docs.python-requests.org/en/master/ for requests library.
'''

import requests

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
    # This value will be set in XoxzoClient.errors when Requests throw exception.
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
        self.xoxzo_api_dins_url = api_host + "/voice/dins/"

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

        payload = {
            'message': message,
            'recipient': recipient,
            'sender': sender}
        try:
            req_res = requests.post(
                self.xoxzo_api_sms_url,
                data=payload,
                auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr =  XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
            return xr
        else:
            if req_res.status_code == 201:
                # when success, return list
                xr = XoxzoResponse(messages=req_res.json())
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def get_sms_delivery_status(self, msgid):
        '''
        Get sms delivery status.

        :param string msgid: msgid of the return value of send_sms() method.
        :return: if XoxzoResponse.errors == None, list of message ids are returned in XoxzoResponse.messages.
            otherwise, error coed is retruned in XoxzoResponse.errors and detailed error message is set in
            XoxzoResponse.message.
        :rtype: XoxzoResponse
        '''

        url = self.xoxzo_api_sms_url + msgid
        try:
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
            return xr
        else:
            if req_res.status_code == 200:
                xr = XoxzoResponse(message=req_res.json())
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def get_sent_sms_list(self, sent_date=None):
        '''
        Get sent messages list

        :param string sent_date: search condition date string.
            see http://docs.xoxzo.com/en/sms.html#sent-messages-list-api.
        :return: if XoxzoResponse.errors == None, list of message ids are returned in XoxzoResponse.messages.
            otherwise, error coed is retruned in XoxzoResponse.errors and detailed error message is set in
            XoxzoResponse.message.
        :rtype: XoxzoResponse
        '''

        if sent_date is None:
            url = self.xoxzo_api_sms_url
        else:
            url = self.xoxzo_api_sms_url + '?sent_date' + sent_date
        try:
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message={"http_error": e})
            return xr
        else:
            if req_res.status_code == 200:
                xr = XoxzoResponse(messages=req_res.json())
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def call_simple_playback(self, caller, recipient, recording_url):
        '''
        Make a phone call and playback MP3 sound file.

        :param string caller: caller phone number.
        :param string recipient: Phone call recipient.
        :param string recording_url: MP3 file URL.
        :return: if XoxzoResponse.errors == None, list of message ids are returned in XoxzoResponse.messages.
            otherwise, error coed is retruned in XoxzoResponse.errors and detailed error message is set in
            XoxzoResponse.message.
        :rtype: XoxzoResponse
        '''

        payload = {
            'caller': caller,
            'recipient': recipient,
            'recording_url': recording_url}

        try:
            req_res = requests.post(
                self.xoxzo_api_voice_simple_url,
                data=payload,
                auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
            return xr
        else:
            if req_res.status_code == 201:
                xr = XoxzoResponse(messages=req_res.json())
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def get_simple_playback_status(self, callid):
        '''
        Get simple palyback status.

        :param string callid: callid of the return value of
            call_simple_playback() method.
        :return: if XoxzoResponse.errors == None, list of message ids are returned in XoxzoResponse.messages.
            otherwise, error coed is retruned in XoxzoResponse.errors and detailed error message is set in
            XoxzoResponse.message.
        :rtype: XoxzoResponse.
        '''

        url = self.xoxzo_api_voice_simple_url + callid
        try:
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message= {"http_error":e})
            return xr
        else:
            if req_res.status_code == 200:
                xr = XoxzoResponse(message=req_res.json())
            elif req_res.status_code == 404:
                # todo: is this really ok???
                xr = XoxzoResponse(errors=req_res.status_code)
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def get_din_list(self, search_string=None):
        """
        get din list
        :param search_string: eg.'country=JP', 'prefix=813'
        :return:
        """
        if search_string == None:
            url = self.xoxzo_api_dins_url
        else:
            url = self.xoxzo_api_dins_url + '?' + search_string
        try:
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message={"http_error": e})
            return xr
        else:
            if req_res.status_code == 200:
                xr = XoxzoResponse(messages=req_res.json())
            elif req_res.status_code == 404:
                # todo: is this really ok???
                xr = XoxzoResponse(errors=req_res.status_code)
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def subscribe_din(self, din_uid=None):
        """
        subscribe DIN
        :param din_uid:
        :return:
        """
        url = self.xoxzo_api_dins_url + 'subscriptions/'

        payload = {
            'din_uid': din_uid
        }

        try:
            req_res = requests.post(url,
                                    data=payload,
                                    auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message={"http_error": e})
            return xr
        else:
            if req_res.status_code == 201:
                xr = XoxzoResponse(messages=req_res.json())
            elif req_res.status_code == 404:
                # todo: is this really ok???
                xr = XoxzoResponse(errors=req_res.status_code)
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def unsubscribe_din(self, din_uid):
        """
        subscribe DIN
        :param din_uid:
        :return:
        """
        url = self.xoxzo_api_dins_url + 'subscriptions/' + din_uid

        try:
            req_res = requests.delete(url, auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message={"http_error": e})
            return xr
        else:
            if req_res.status_code == 200:
                xr = XoxzoResponse()
            elif req_res.status_code == 404:
                # todo: is this really ok???
                xr = XoxzoResponse(errors=req_res.status_code)
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr

    def get_subscription_list(self):
        """

        :return:
        """
        url = self.xoxzo_api_dins_url + 'subscriptions/'

        try:
            req_res = requests.get(url, auth=(self.sid, self.auth_token))
        except requests.exceptions.RequestException as e:
            xr = XoxzoResponse(errors=XoxzoClient.REQUESTS_EXCEPITON, message={"http_error": e})
            return xr
        else:
            if req_res.status_code == 200:
                xr = XoxzoResponse(messages=req_res.json())
            elif req_res.status_code == 404:
                # todo: is this really ok???
                xr = XoxzoResponse(errors=req_res.status_code)
            else:
                xr = XoxzoResponse(
                    errors=req_res.status_code,
                    message=req_res.json())
            return xr
