# -*- coding: utf-8 -*-

"""
Xoxzo Cloud API Client for Python
~~~~~~~~~~~~~~~~~~~~~
xoxzo.cloudpy is the python package that you can send sms or make a phone call
and playback a MP3 file via Xoxzo telephony API.

# Send sms sample code
def sample_send_sms():
   xc = XoxzoClient(sid="<your xoxzo sid>",
                    auth_token="<your xoxzo auth_token>")
   result = xc.send_sms(message = "Hello from Xoxzo",
                        recipient = "+818012345678",
                        sender = "818011112222")
   if result.errors != None:
       # some error happened
       print json.dumps(result.message, indent=4)
   else:
       # check messge delivery status
       msgid = result.messages[0]['msgid']
       result = xc.get_sms_delivery_status(msgid)
       print json.dumps(result.message, indent=4)

# Make a phone call and playback MP3 file sample code
def sample_call_simple_playback():
   xc = XoxzoClient(sid="<your xoxzo sid>",
                    auth_token="<your xoxzo auth_token>")
   result = xc.call_simple_playback(
       recipient="+818012345678",
       recording_url="http://example.com/sample.mp3",
       caller="818011112222")
   if result.errors != None:
       # some error happened
       print json.dumps(result.message, indent=4)
   else:
       callid = result.messages[0]['callid']
       result = xc.get_simple_playback_status(callid)
       print json.dumps(result.message, indent=4)

...

More methods are supported. For detailed documentation on the API itself,
you can refer to the documentation at <http://docs.xoxzo.com>.

:copyright: (c) 2017 by Xoxzo Inc.
:license: The MIT License (MIT), see LICENSE for details.
"""

from .cloudpy import XoxzoClient
