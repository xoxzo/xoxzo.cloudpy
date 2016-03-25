# -*- coding: utf-8 -*-
import unittest
import json
import os

from xoxzo.cloudpy import XoxzoClient


class TestXoxzoClient(unittest.TestCase):
    def setUp(self):
        self.test_recipient = os.environ.get("XOXZO_API_TEST_RECIPIENT")
        self.test_sender = "04512345678"
        print "Test recipient: %s" % self.test_recipient
        print "Test sender: %s" % self.test_sender

    def test_send_sms_success(self):
        xc = XoxzoClient()
        response = xc.send_sms(
            "Hello from Xoxzo",
            self.test_recipient,
            self.test_sender)
        self.dump_response(response)
        # get msgid from response
        # msgid = response.json()[0]['msgid']
        response = xc.get_sms_delivery_status()
        self.dump_response(response)

    def dump_response(self, response):
        print json.dumps(response.json(), indent=4)
