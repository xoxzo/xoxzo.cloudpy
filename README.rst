=====================================
Xoxzo Cloud API Client for Python
=====================================

This is the official client and implementation reference to talk to `Xoxzo's Cloud Communication API <https://www.xoxzo.com/en/>`_.
For detailed documentation on the API itself, you can refer to the `documentation <http://docs.xoxzo.com/en/>`_

**sample code**

send sms::

  import json
  from xoxzo.cloudpy import XoxzoClient

  # sample 01 send sms
  xc = XoxzoClient(sid="<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
  xc.send_sms(
      message = "Hello from Xoxzo",
      recipient = "+818012345678",
      sender = "818011112222")
  result = xc.get_sms_delivery_status()
  print json.dumps(result.json(), indent=4)


play back mp3 file::

  # sample 02 call voice playback

  xc = XoxzoClient(sid="<your xoxzo sid>", auth_token="<your xoxzo auth_token>")
  xc.call_simple_playback(
      recipient = "+818012345678",
      recording_url = "http://example.com/sample.mp3",
      caller = "818011112222")
  result = xc.get_simple_playback_status()
  print json.dumps(result.json(), indent=4)
