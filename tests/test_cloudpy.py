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

        # print
        # print "Test recipient: %s" % self.test_recipient
        # print "Test sender: %s" % self.test_sender
        # print "Test MP3 url: %s" % self.test_mp3_url

    def test_send_sms_success01(self):
        return  # skip for now
        xc = XoxzoClient()
        response = xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        self.dump_response(response)

        response = xc.get_sms_delivery_status()
        self.dump_response(response)

    def test_call_simple_playback_success01(self):
        return  # skip for now
        xc = XoxzoClient()
        response = xc.call_simple_playback(
            self.test_sender,
            self.test_recipient,
            self.test_mp3_url)

        self.dump_response(response)

        response = xc.get_simple_playback_status()
        self.dump_response(response)

    def test_bad_sid(self):
        xc = XoxzoClient(sid = "123", auth_token = "456")
        response = xc.send_sms(
            message = "Hello from Xoxzo",
            recipient = "+8108012345678",
            sender = self.test_sender)
        self.dump_response(response)

    def test_send_sms_fail01(self):
        # bad recipient
        xc = XoxzoClient()
        response = xc.send_sms(
            message = "Hello from Xoxzo",
            recipient = "+8108012345678",
            sender = self.test_sender)

        self.dump_response(response)

    def test_get_sms_delivery_status_fail01(self):
        # bad msgid
        xc = XoxzoClient()
        response = xc.get_sms_delivery_status(msgid = "dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.dump_response(response)

    def test_call_simple_playback_fail01(self):
        # bad recipient
        xc = XoxzoClient()
        response = xc.call_simple_playback(
            self.test_sender,
            "+8108012345678",
            self.test_mp3_url)
        self.dump_response(response)

    def test_get_simple_playback_status_fail01(self):
        # bad callid
        xc = XoxzoClient()
        response = xc.get_simple_playback_status(callid = "dabd8e76-390f-421c-87b5-57f31339d0c5")
        self.dump_response(response)

    def dump_response(self, response):
        print
        print type(response)
        print json.dumps(response, indent=4)

if __name__ == "__main__":
        unittest.main()
