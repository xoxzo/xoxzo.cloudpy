# xoxzo api libirary

import urllib
import urllib2

def send_sms_message(sid, auth_token,message,recipient,sender):
    url = "https://api.xoxzo.com/sms/messages/"
    user_agent = "xoxzo cloudpy 1.0"
    values = {'message' : message,
              'recipient' : recipient,
              'sender' : sender }

    headers = { 'User-Agent' : user_agent }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)

    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of ``None``.
    password_mgr.add_password(None, url, sid, auth_token)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

    response = urllib2.urlopen(req)
    return response.read()
