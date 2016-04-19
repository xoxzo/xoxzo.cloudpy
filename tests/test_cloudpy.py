# -*- coding: utf-8 -*-
import unittest
import json
import os
import requests

from xoxzo.cloudpy import XoxzoClient


class TestXoxzoClient(unittest.TestCase):
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
        self.assertTrue('detail' in xoxzo_res.message)

    def test_requests_exceeption_send_sms(self):
        # inject bad api url
        self.xc.xoxzo_api_sms_url="example.com"

        xoxzo_res = self.xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)

    def test_requests_exceeption_get_sms_delivery_status(self):
        # inject bad api url
        self.xc.xoxzo_api_sms_url = "example.com"

        xoxzo_res = self.xc.get_sms_delivery_status("1234567890")
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)

    def test_requests_exceeption_get_sent_sms_list(self):
        # inject bad api url
        self.xc.xoxzo_api_sms_url = "example.com"

        xoxzo_res = self.xc.get_sent_sms_list()
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)

    def test_requests_exceeption_call_simple_playback(self):
        # inject bad api url
        self.xc.xoxzo_api_voice_simple_url = "example.com"

        xoxzo_res = self.xc.call_simple_playback(
            self.test_sender,
            self.test_recipient,
            self.test_mp3_url)
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)

    def test_requests_exceeption_get_simple_playback_status(self):
        # inject bad api url
        self.xc.xoxzo_api_voice_simple_url = "example.com"
        xoxzo_res = self.xc.get_simple_playback_status(
            callid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(xoxzo_res.errors, XoxzoClient.REQUESTS_EXCEPITON)

    # SMS Tests
    @unittest.skip("skip this for now")
    def test_send_sms_success01(self):
        xoxzo_res = self.xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        self.assertEqual(xoxzo_res.errors, None)
        msgid = xoxzo_res.messages[0]['msgid']
        response = self.xc.get_sms_delivery_status(msgid)
        self.assertEqual(response.errors, None)

    def test_send_sms_fail01(self):
        # bad recipient
        xoxzo_res = self.xc.send_sms(
            message="Hello from Xoxzo",
            recipient="+8108012345678",
            sender=self.test_sender)
        self.assertEqual(xoxzo_res.errors, 400)
        self.assertTrue('recipient' in xoxzo_res.message)

    def test_get_sms_delivery_status_fail01(self):
        # bad msgid
        xoxzo_res = self.xc.get_sms_delivery_status(
            msgid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(xoxzo_res.errors, 404)
        # currentry this asssertion fails due to bug
        self.assertEqual(xoxzo_res.message, None)

    def test_get_sms_list_success01(self):
        xoxzo_res = self.xc.get_sent_sms_list()
        self.assertEqual(xoxzo_res.errors, None)

    def test_get_sms_list_success02(self):
        xoxzo_res = self.xc.get_sent_sms_list(sent_date=">=2016-04-01")
        self.assertEqual(xoxzo_res.errors, None)

    def test_get_sms_list_fail01(self):
        # bad date string
        xoxzo_res = self.xc.get_sent_sms_list(sent_date=">=2016-13-01")
        self.assertEqual(xoxzo_res.errors, 400)
        self.assertTrue('sent_date' in xoxzo_res.message)

    # Voice Tests
    @unittest.skip("skip this for now")
    def test_call_simple_playback_success01(self):
        xoxzo_res = self.xc.call_simple_playback(
            self.test_sender,
            self.test_recipient,
            self.test_mp3_url)
        self.assertEqual(xoxzo_res.errors, None)
        callid = xoxzo_res.messages[0]['callid']
        xoxzo_res = self.xc.get_simple_playback_status(callid)
        self.assertEqual(xoxzo_res.errors, None)

    def test_call_simple_playback_fail01(self):
        # bad recipient
        xoxzo_res = self.xc.call_simple_playback(
            self.test_sender,
            "+8108012345678",
            self.test_mp3_url)
        self.assertEqual(xoxzo_res.errors, 400)
        self.assertTrue('recipient' in xoxzo_res.message)

    def test_get_simple_playback_status_fail01(self):
        # bad callid
        xoxzo_res = self.xc.get_simple_playback_status(
            callid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(xoxzo_res.errors, 404)
        # currentry this asssertion fails due to bug
        self.assertEqual(xoxzo_res.messages, None)

    def dump_response(self, response):
        print
        print type(response)
        print "errors:" + response.errors
        print "message:\n" + json.dumps(response.message, indent=4)
        print "messages:\n" + json.dumps(response.messages, indent=4)

if __name__ == "__main__":
    unittest.main()
