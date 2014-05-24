"""

"""
from django.test import TestCase
from django.test.client import Client

from noodles.ecommerce.views import PayPalListener
from noodles.ecommerce.util import generate_ipn_postback_data


class UtilTestCase(TestCase):
    """
    Test cases regarding utility functions for the ecommerce module
    """
    
    def setUp(self):
        """
        Set a few things up
        """
        self.correct = {
            "invoice": "asdfasdf",
            "txn_id": "asdf",
            "receiver_email": "brantm_1301423087_biz@gmail.com",
            "mc_gross": "875.00",
            "mc_currency": "USD",
        }
    
    def test_ipn_postback_generator(self):
        """
        Test that our postback generator spits out what we want it to
        """
        self.assertEquals(generate_ipn_postback_data(self.correct), "cmd=_notify-validate&receiver_email=brantm_1301423087_biz@gmail.com&mc_gross=875.00&txn_id=asdf&mc_currency=USD&invoice=asdfasdf")
        self.assertEquals(generate_ipn_postback_data(self.correct), "cmd=_notify-validate&receiver_email=brantm_1301423087_biz@gmail.com&mc_gross=875.00&txn_id=asdf&mc_currency=USD&invoice=asdfasdf")

