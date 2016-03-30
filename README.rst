=====================================
Xoxzo Cloud API Client for Python
=====================================

This is the official client and implementation reference to talk to `Xoxzo's Cloud Communication API <https://www.xoxzo.com/en/>`_.
For detailed documentation on the API itself, you can refer to the `documentation <http://docs.xoxzo.com/en/>`_

**About**

xoxzo.cloudpy is the paython package that you can send sms or make a phone call and playback a MP3 file
via Xoxzo telephony API. This is the open source package with XXX LICENSE.

**Sample Code**

*send sms*::

  import json
  from xoxzo.cloudpy import XoxzoClient

  # sample 01 send sms
  def sample_send_sms():
      xc = XoxzoClient(sid="<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
      result = xc.send_sms(
          message = "Hello from Xoxzo",
          recipient = "+818012345678",
          sender = "818011112222")
      if not isinstance(result,list):
          print "*** Error ***"
          print result['detail']
          return

      result = xc.get_sms_delivery_status(msgid)
      print json.dumps(result, indent=4)

  sample_send_sms()

**How to use**

You can send sms or make a phone call with just a few line of python code.

1. First, you need to create XoxzoClient() object. You must provide xoxzo sid and auth_token when initializing this object. You can get sid and auth_token after you sign up the xoxzo account and access the xoxzo dashboard.


2. Then you can call send_sms() method. You need to provide three parameters.

  * message: sms text you want to send.

  * recipient: phone number of the sms recipient. This must start with Japanese country code "+81" and follow the
    `E.164 <https://en.wikipedia.org/wiki/E.164>`_ format.

  * sender: this number will be displayed on the recipient device.

  This method will return json or list. If there is no error, list that contains the message-id will be returned.
  You will need this id when checking the delivery status later.

3. You can check the sms delivery status by get_sms_delivery_status() method. You will provide message-id of the sms you want to check.
