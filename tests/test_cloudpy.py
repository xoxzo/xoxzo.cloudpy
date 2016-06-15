# -*- coding: utf-8 -*-
import json
import os
import unittest

from xoxzo.cloudpy import XoxzoClient


class TestXoxzoClientTestCase(unittest.TestCase):
    def setUp(self):
        self.test_recipient = os.environ.get("XOXZO_API_TEST_RECIPIENT")
        self.test_sender = "814512345678"
        self.test_mp3_url = os.environ.get("XOXZO_API_TEST_MP3")
        sid = os.environ.get("XOXZO_API_SID")
        auth_token = os.environ.get("XOXZO_API_AUTH_TOKEN")
        self.xc = XoxzoClient(sid=sid, auth_token=auth_token)

        # print
        # print "Test recipient: %s" % self.test_recipient
        # print "Test sender: %s" % self.test_sender
        # print "Test MP3 url: %s" % self.test_mp3_url

    # Generic Tests
    def test_bad_sid(self):
        bad_xc = XoxzoClient(sid="123", auth_token="456")
        xoxzo_res = bad_xc.send_sms(
            message="Hello from Xoxzo",
            recipient="+8108012345678",
            sender=self.test_sender)
        self.assertEqual(xoxzo_res.errors, 401)
        self.assertEqual(xoxzo_res.messages, [])
        self.assertTrue('detail' in xoxzo_res.message)

    def test_requests_exception_send_sms(self):
        # inject bad api url
        self.xc.xoxzo_api_sms_url="example.com"

        xoxzo_res = self.xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)
        self.assertTrue("http_error" in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])


    def test_requests_exception_get_sms_delivery_status(self):
        # inject bad api url
        self.xc.xoxzo_api_sms_url = "example.com"

        xoxzo_res = self.xc.get_sms_delivery_status("1234567890")
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)
        self.assertTrue("http_error" in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    def test_requests_exception_get_sent_sms_list(self):
        # inject bad api url
        self.xc.xoxzo_api_sms_url = "example.com"

        xoxzo_res = self.xc.get_sent_sms_list()
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)
        self.assertTrue("http_error" in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    def test_requests_exception_call_simple_playback(self):
        # inject bad api url
        self.xc.xoxzo_api_voice_simple_url = "example.com"

        xoxzo_res = self.xc.call_simple_playback(
            self.test_sender,
            self.test_recipient,
            self.test_mp3_url)
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)
        self.assertTrue("http_error" in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    def test_requests_exceeption_get_simple_playback_status(self):
        # inject bad api url
        self.xc.xoxzo_api_voice_simple_url = "example.com"
        xoxzo_res = self.xc.get_simple_playback_status(
            callid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)
        self.assertTrue("http_error" in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    # SMS Tests
    @unittest.skip("skip this for now")
    def test_send_sms_success01(self):
        xoxzo_res = self.xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        self.assertEqual(xoxzo_res.errors, None)
        self.assertEqual(xoxzo_res.message,{})
        self.assertTrue('msgid' in xoxzo_res.messages[0])

        msgid = xoxzo_res.messages[0]['msgid']
        xoxzo_res = self.xc.get_sms_delivery_status(msgid)
        self.assertEqual(xoxzo_res.errors, None)
        self.assertTrue('msgid' in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages,[])

    def test_send_sms_fail01(self):
        # bad recipient
        xoxzo_res = self.xc.send_sms(
            message="Hello from Xoxzo",
            recipient="+8108012345678",
            sender=self.test_sender)
        self.assertEqual(xoxzo_res.errors, 400)
        self.assertTrue('recipient' in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    def test_get_sms_delivery_status_fail01(self):
        # bad msgid
        xoxzo_res = self.xc.get_sms_delivery_status(
            msgid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(xoxzo_res.errors, 404)
        # todo: currentry this asssertion fails due to bug X4CTBE-112
        # self.assertEqual(xoxzo_res.message, None)
        # self.assertEqual(xoxzo_res.messages, [])

    def test_get_sms_list_success01(self):
        xoxzo_res = self.xc.get_sent_sms_list()
        self.assertEqual(xoxzo_res.errors, None)
        self.assertEqual(xoxzo_res.message, {})
        self.assertEqual(type(xoxzo_res.messages), list)

    def test_get_sms_list_success02(self):
        xoxzo_res = self.xc.get_sent_sms_list(sent_date=">=2016-04-01")
        self.assertEqual(xoxzo_res.errors, None)
        self.assertEqual(xoxzo_res.message, {})
        self.assertEqual(type(xoxzo_res.messages), list)

    def test_get_sms_list_fail01(self):
        # bad date string
        xoxzo_res = self.xc.get_sent_sms_list(sent_date=">=2016-13-01")
        self.assertEqual(xoxzo_res.errors, 400)
        self.assertTrue('sent_date' in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    # Voice Tests
    @unittest.skip("skip this for now")
    def test_call_simple_playback_success01(self):
        xoxzo_res = self.xc.call_simple_playback(
            self.test_sender,
            self.test_recipient,
            self.test_mp3_url)
        self.assertEqual(xoxzo_res.errors, None)
        self.assertEqual(xoxzo_res.message, {})
        self.assertTrue('callid' in xoxzo_res.messages[0])

        callid = xoxzo_res.messages[0]['callid']
        xoxzo_res = self.xc.get_simple_playback_status(callid)
        self.assertEqual(xoxzo_res.errors, None)
        self.assertTrue('callid' in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    def test_call_simple_playback_fail01(self):
        # bad recipient
        xoxzo_res = self.xc.call_simple_playback(
            self.test_sender,
            "+8108012345678",
            self.test_mp3_url)
        self.assertEqual(xoxzo_res.errors, 400)
        self.assertTrue('recipient' in xoxzo_res.message)
        self.assertEqual(xoxzo_res.messages, [])

    def test_get_simple_playback_status_fail01(self):
        # bad callid
        xoxzo_res = self.xc.get_simple_playback_status(
            callid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(xoxzo_res.errors, 404)
        # todo: currentry this asssertion fails due to bug X4CTBE-113
        # self.assertEqual(xoxzo_res.message, None)
        self.assertEqual(xoxzo_res.messages, [])

    def test_get_din_list_success(self):
        xoxzo_res = self.xc.get_din_list()
        self.assertEqual(xoxzo_res.errors, None)

    def test_get_din_list_prefix_success01(self):
        xoxzo_res = self.xc.get_din_list(search_string='country=JP')
        self.assertEqual(xoxzo_res.errors, None)

    def test_get_din_list_prefix_success02(self):
        xoxzo_res = self.xc.get_din_list(search_string='country=US')
        self.assertEqual(xoxzo_res.errors, None)

    def test_get_din_list_prefix_success03(self):
        xoxzo_res = self.xc.get_din_list(search_string='prefix=813')
        self.assertEqual(xoxzo_res.errors, None)

    def test_get_din_list_fail01(self):
        xoxzo_res = self.xc.get_din_list(search_string="foo=bar")
        self.assertEqual(xoxzo_res.errors, 400)
        # self.dump_response(xoxzo_res)

    def dump_response(self, response):
        print("===== DUMP RESPONSE =====")
        if (response.errors != None):
            print("errors:" + str(response.errors))
        print("message:\n" + self.my_json_dumps(response.message))
        print("messages:\n" + self.my_json_dumps(response.messages))

    def my_json_dumps(self, data):
        if (data != None):
            return json.dumps(data, indent=4)


if __name__ == "__main__":
    unittest.main()
