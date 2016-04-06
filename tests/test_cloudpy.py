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

    @unittest.skip("skip this for now")
    def test_send_sms_success01(self):
        response = self.xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        msgid = response[0]['msgid']
        response = self.xc.get_sms_delivery_status(msgid)
        self.assertTrue('status' in response)

    @unittest.skip("skip this for now")
    def test_call_simple_playback_success01(self):
        response = self.xc.call_simple_playback(
            self.test_sender,
            self.test_recipient,
            self.test_mp3_url)

        callid = response[0]['callid']
        response = self.xc.get_simple_playback_status(callid)
        self.dump_response(response)
        self.assertTrue('status' in response)

    def test_bad_sid(self):
        bad_xc = XoxzoClient(sid="123", auth_token="456")
        response = bad_xc.send_sms(
            message="Hello from Xoxzo",
            recipient="+8108012345678",
            sender=self.test_sender)
        self.assertTrue('detail' in response)

    def test_send_sms_fail01(self):
        # bad recipient
        response = self.xc.send_sms(
            message="Hello from Xoxzo",
            recipient="+8108012345678",
            sender=self.test_sender)
        self.assertTrue('recipient' in response)

    def test_get_sms_delivery_status_fail01(self):
        # bad msgid
        response = self.xc.get_sms_delivery_status(
            msgid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(response, [])

    def test_get_sms_list_success01(self):
        response = self.xc.get_sms_list()
        self.assertTrue(isinstance(response, list))

    def test_get_sms_list_success02(self):
        response = self.xc.get_sms_list(sent_date=">=2016-04-01")
        self.assertTrue(isinstance(response, list))

    def test_get_sms_list_fail01(self):
        # bad date string
        response = self.xc.get_sms_list(sent_date=">=2016-13-01")
        self.assertTrue(isinstance(response, dict))
        self.assertTrue('sent_date' in response)

    def test_call_simple_playback_fail01(self):
        # bad recipient
        response = self.xc.call_simple_playback(
            self.test_sender,
            "+8108012345678",
            self.test_mp3_url)
        self.assertTrue('recipient' in response)

    def test_get_simple_playback_status_fail01(self):
        # bad callid
        response = self.xc.get_simple_playback_status(
            callid="dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.assertEqual(response, [])

    def dump_response(self, response):
        print
        print type(response)
        print json.dumps(response, indent=4)

if __name__ == "__main__":
        unittest.main()
