=================================
Xoxzo Cloud API Client for Python
=================================

This is the official client and implementation reference to talk to `Xoxzo's Cloud Communication API <https://www.xoxzo.com/en/>`_.
For detailed documentation on the API itself, you can refer to the `documentation <http://docs.xoxzo.com/en/>`_


**Introduction**
-------------------

xoxzo.cloudpy is the python package that you can send sms or make a phone call and playback a MP3 file
via Xoxzo telephony API. This is the open source package with MIT LICENSE.


**Sample Code 1**
-------------------

*Send sms*::

 def sample_send_sms():
    xc = XoxzoClient(sid="<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
    result = xc.send_sms(
        message = "Hello from Xoxzo",
        recipient = "+818012345678",
        sender = "818011112222")
    if result.errors != None:
        # some error happed
        print json.dumps(result.message, indent=4)
    else:
        # check messge delivery status
        msgid = result.messages[0]['msgid']
        result = xc.get_sms_delivery_status(msgid)
        print json.dumps(result.message, indent=4)

*Explanation*

You can send sms or make a phone call with just a few line of python code.

1. First, you need to create XoxzoClient() object. You must provide xoxzo sid and auth_token when initializing this object. You can get sid and auth_token after you sign up the xoxzo account and access the xoxzo dashboard.

2. Then you can call send_sms() method. You need to provide three parameters.

  * message: sms text you want to send.

  * recipient: phone number of the sms recipient. This must start with Japanese country code "+81" and follow the
    `E.164 <https://en.wikipedia.org/wiki/E.164>`_ format.

  * sender: this number will be displayed on the recipient device.

  This method will return XoxzoResponse object. If XoxzoResponse.errors == None, XoxzoResponse.messages[0]['msgid']
  is the meesage id that you can pass to the get_sms_delivery_status() call.

3. You can check the sms delivery status by get_sms_delivery_status() method. You will provide message-id of the sms you want to check.

*Check SMS sent status*::

 xoxzo_res = xc.get_sent_sms_list(sent_date=">=2016-13-01")

*Explanation*

You can check sent SMS status specifying a certain date. You can use comparison operators such as "<=,<,=,>,>="


**Sample Code 2**
-------------------

*Make a phone call and playback MP3 file*::

 def sample_call_simple_playback():

    xc = XoxzoClient(sid="<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
    result = xc.call_simple_playback(
        recipient="+818012345678",
        recording_url="http://example.com/sample.mp3",
        caller="818011112222")

    if result.errors != None:
        # some error happed
        print json.dumps(result.message, indent=4)
    else:
        callid = result.messages[0]['callid']
        result = xc.get_simple_playback_status(callid)
        print json.dumps(result.message, indent=4)

*Explanation*

1. First, you need to create XoxzoClient() object. You must provide xoxzo sid and auth_token when initializing this object. You can get sid and auth_token after you sign up the xoxzo account and access the xoxzo dashboard.

2. Then you can call call_simple_playback() method. You need to provide three parameters.

  * recording_url: URL of the MP3 file you want to playback.

  * recipient: phone number of the call recipient. This must start with Japanese country code "+81" and follow the
    `E.164 <https://en.wikipedia.org/wiki/E.164>`_ format.

  * caller: this number will be displayed on the recipient device.

  This method will return XoxzoResponse object. If XoxzoResponse.errors == None, XoxzoResponse.messages[0]['callid']
  is the meesage id that you can pass to the get_sms_delivery_status() call.

3. You can check the call status by get_simple_playback_status() method. You will provide call-id of the call you want to check.


**Sample Code 3**
-------------------

*Make a phone call and playback TTS message*::

 def sample_call_tts_playback():

    xc = XoxzoClient(sid= "<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
    result = xc.call_tts_playback(
        caller="818011112222",
        recipient="+818012345678",
        tts_message="Hello",
        tts_lang="ja")

    if result.errors != None:
        # some error happed
        print json.dumps(result.message, indent=4)
    else:
        callid = result.messages[0]['callid']
        result = xc.get_simple_playback_status(callid)
        print json.dumps(result.message, indent=4)

*Explanation*

1. First, you need to create XoxzoClient() object. You must provide xoxzo sid and auth_token when initializing this object. You can get sid and auth_token after you sign up the xoxzo account and access the xoxzo dashboard.

2. Then you can call call_tts_playback() method. You need to provide four parameters.

  * caller: this number will be displayed on the recipient device.

  * recipient: phone number of the call recipient. This must start with Japanese country code "+81" and follow the
    `E.164 <https://en.wikipedia.org/wiki/E.164>`_ format.

  * tts_message: TTS text message you want to playback.

  * tts_lang: language code of TTS call.

  This method will return XoxzoResponse object. If XoxzoResponse.errors == None, XoxzoResponse.messages[0]['callid']
  is the meesage id that you can pass to the get_sms_delivery_status() call.

3. You can check the call status by get_simple_playback_status() method. You will provide call-id of the call you want to check.


**Sample Code 4**
-------------------

*Subscribe DIN*::

 xc = XoxzoClient(sid="<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
 xoxzo_res = xc.get_din_list()
 din_uid = xoxzo_res.messages[0]['din_uid']
 xoxzo_res = xc.subscribe_din(din_uid=din_uid)

*Explanation*

1. In order to subscribe DIN, you must find available unsubscribed DINs using get_din_list() method.

2. Then you subscribe a DIN via subscribe_din() method specifying din unique id.

*Set action URL*::

 an_action_url = 'http://example.com/dummy_action'
 xoxzo_res = xc.set_action_url(din_uid=din_uid, action_url=an_action_url)

*Explanation*

1. Once you subscribed the DIN, you can set action url to the DIN. This URL will be called in the event of the DIN gets called.
The URL will called by http GET method with the parameters, caller and recipient.

*Get the list of subscription*::

 xoxzo_res = self.xc.get_subscription_list()

*Explanation*

In order to get the list of current subscriptions, you can call the method above.


*Unsubscribe DIN*::

   xoxzo_res = self.xc.unsubscribe_din(din_uid=din_uid)

*Explanation*

1. When you no longer use DIN, you can unsubscribe the DIN by specifying the din unique id.
