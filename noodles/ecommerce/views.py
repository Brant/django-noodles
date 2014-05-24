"""
PayPal Transaction Views

Usually not directly hittable...

e.g. Used to interface with paypal IPN
"""

import urllib

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import  mail_admins
from django.views.generic.base import View


from noodles.ecommerce.util import generate_ipn_postback_data
from noodles.ecommerce.models import PayPalPayment
from noodles.ecommerce.exceptions import PayPalError, PayPalMissingValueError, PayPalRecieverError 
from noodles.ecommerce.exceptions import PayPalGrossTotalError, UnimplementedPaypalListenerMethod, PayPalAlreadyPaidError


class BasePayPalListener(View):
    """
    Base view for creating PayPal Listeners
    
    Certain methods must be implemented by the subclass
        - get_total
        - get_purchase
        - do_after_payment (optional)
    """
    
    # tuple: (<paypal post data name>, <foundation model field name>)
    _important = (
            ("txn_id", "transaction"),
            ("first_name", "first_name"),
            ("last_name", "last_name"),
            ("payer_email", "email"),
            ("address_name", "shipping_name"),
            ("address_street", "street"),
            ("address_city", "city"),
            ("address_state", "state"),
            ("address_zip", "zip"),
            ("address_country", "country"),
    )
    
    def get_base_price(self, postdata):
        gross = float(postdata["mc_gross"])
        
        try:
            tax = postdata["tax"]
        except MultiValueDictKeyError:
            tax = 0
        tax = float(tax)
        
        try:
            shipping = postdata["shipping"]
        except MultiValueDictKeyError:
            shipping = 0
        shipping = float(shipping)
        
        return "%.2f" % (gross - (tax + shipping))
        
    
    def __init__(self, **kwargs):
        """
        These are things that will be needed later.
        
        They are actually set within other methods
            see: PayPalListener for things to override
        
        """
        
        self.invoice = None
        self.purchase = None
        self.ipn_url = None
        self.payment_reciever = None
        self.is_refund = False
        self.thankyou_message = "Thanks"
        
        super(BasePayPalListener, self).__init__(**kwargs)
    
    def get_paypal_important_meta(self):
        """
        Important pieces from paypal's POST data that we need to store
        paired with attributes of our PayPalPayment model
        
        key:
        paypal: model
        """
        return self._important
    
    def _retrieve_paypal_verification(self, url_data):
        """
        Send a POST request to a url for paypal verification
        
        Returns response to POST request
        """
        page1 = urllib.urlretrieve(self.ipn_url, data=url_data)
        filename = page1[0]
        the_file = open(filename, "r")
        content = the_file.read()
        the_file.close()
        return content
    
    def is_unpaid(self, txn_id):
        """
        Determine if a given transaction ID already has a payment associated with it
        """
        try:
            PayPalPayment.objects.get(transaction=txn_id)
            PayPalPayment.objects.get(invoice=self.invoice)
            return False
        except ObjectDoesNotExist:
            return True
        
    def check_post_data(self, postdata):
        """
        Checks some important keys
        
        Raises errors
        """
        if not postdata.has_key("receiver_email"):
            raise PayPalMissingValueError("No receiver_email in post data")
            
        if not postdata.has_key("mc_gross"):                
            raise PayPalMissingValueError("No mc_gross in post data")
        
        if not postdata.has_key("mc_currency"):
            raise PayPalMissingValueError("No mc_currency in post data")
        
        if not postdata['receiver_email'].lower() == self.payment_reciever.lower():
            raise PayPalRecieverError("reciever_email did not match paypal_meta's receiver email (%s and %s)" % (postdata['receiver_email'], self.payment_reciever))
        
        if not self.get_total():
            raise UnimplementedPaypalListenerMethod("Method get_total unimplemented for PayPalListener subclass")
        
        
        base_price = self.get_base_price(postdata)
        
        if postdata['payment_status'] == "Refunded":
            return self.send_thanks()
#            if not base_price == "-%s" % self.get_total():
#                raise PayPalGrossTotalError("mc_gross did not match total calculated by PayPal Listener: %s vs -%s" % (base_price, self.get_total()))
#            self.is_refund = True
            
        elif postdata['payment_status'] == "Completed":
            if not base_price == self.get_total():
                raise PayPalGrossTotalError("mc_gross did not match total calculated by PayPal Listener: %s vs %s" % (base_price, self.get_total()))

    def create_payment(self, postdata):
        """
        Create the payment information
        
        Post data really only needs to contain "invoice" and "txn_id"
        """
        payment = PayPalPayment()
        problems = ""
        
        payment.invoice = postdata['invoice']
        
        meta = self.get_paypal_important_meta()
        
        for paypal_attr, model_attr in meta:
            if postdata.has_key(paypal_attr):
                setattr(payment, model_attr, postdata[paypal_attr])
            else:
                problems += " | Paypal Response Didn't Contain %s" % paypal_attr
                
        payment.payment_problems = problems
        payment.save()
        
        self.purchase.payment = payment
    
    def mark_as_refund(self, postdata):
        pass
    
    def _validate_setup(self):
        """
        Validates the setup, raises errors before we dive too deep
        """
        if not self.ipn_url:
            raise UnimplementedPaypalListenerMethod("must set ipn_url attribute in setup_listener method")
        
        if not self.payment_reciever:
            raise UnimplementedPaypalListenerMethod("must set payment_reciever attribute in setup_listener method")
   
    def post(self, request):
        """
        Handle paypal's post data being sent
        
        Needs to anaylze and spit back hte data
        """
        self.setup_listener()
        self._validate_setup()
        
        url_data = generate_ipn_postback_data(request.POST)
        
        verification = self._retrieve_paypal_verification(url_data)
        
        if not request.POST.has_key("invoice"):
            raise PayPalMissingValueError
        
        self.invoice = request.POST['invoice']
        
        try:
            self.purchase = self.get_purchase()
        except ObjectDoesNotExist:
            mail_admins("Ecommerce Object: Match Not Found", "From Paypal:\n%s\n\n\nPost data:\n%s" % (verification, request.POST))
            return self.send_thanks()
        
        if not self.purchase:
            raise UnimplementedPaypalListenerMethod("Method: get_purchase not implemented in PayPalListener subclass")
            
        if "%s" % verification == "VERIFIED":
            
            if not request.POST.has_key("txn_id"):
                raise PayPalMissingValueError("No Transaction ID")
            
            if not self.is_unpaid(request.POST['txn_id']):
                raise PayPalAlreadyPaidError("There was an attempt to pay for a purchase which has already been paid for")
            
            self.check_post_data(request.POST)
            
            if self.is_refund:
                self.mark_as_refund(request.POST)
            else:
                self.create_payment(request.POST)
                
            self.do_after_payment()
        else:
            raise PayPalGrossTotalError("Verification from paypal failed")
        
        return self.send_thanks()
    
    def setup_listener(self):
        """
        Override needed by implementing subclass
        """
        self.invoice = None
        self.ipn_url = None
        self.payment_reciever = None
        
    def get_purchase(self):
        """
        To be implemented by subclass
        
        - Return purchase object if successful
        - Raise ObjectDoesNotExist if invoice doesnt match
        - Return None if not implemented
        
        refer to self.invoice
        """
        raise NotImplementedError
    
    def get_total(self):
        """
        All purchases must have some way of calculating a total
        
        Must be implemented by subclass
        - returns None if not implemented
        - returns total (as a string) if implemented for purchase
        """
        raise NotImplementedError
    
    def do_after_payment(self):
        """
        OPtionally implemented by subclass
        
        Will be called after create_payment
        """
        pass
    
    def send_thanks(self):
        """
        Always need to send a message back
        
        Otherwise, paypal keeps sending post
        """
        return HttpResponse(self.thankyou_message)
    
    

class PayPalListener(BasePayPalListener):
    """
    PayPalListener "interface"
    
    These methods must be overridden in order to have a funcitonal listener
    
    Available Attributes (Can be referenced by subclass in methods):
        self.invoice
        self.purchase
        self.ipn_url
        self.payment_reciever
    """
    
    def get_purchase(self):
        """
        To be implemented by subclass
        
        - Return purchase object if successful
        - Raise ObjectDoesNotExist if invoice doesnt match
        - Return None if not implemented
        
        refer to self.invoice if needed for query
        """
        return self.purchase
    
    def get_total(self):
        """
        All purchases must have some way of calculating a total
        
        Must be implemented by subclass
        - returns None if not implemented
        - returns total (as a string) if implemented for purchase
        """
        raise NotImplementedError
    
    def do_after_payment(self):
        """
        OPtionally implemented by subclass
        
        Will be called after create_payment
        """
        pass
    
    
    def setup_listener(self):
        """
        We need to set some class attributes for this all to work
        
        - invoice as defined by the purchase
        - ipn url (either the real paypal ipn api url or the sandbox
        - email of receiver
        """
        self.invoice = None
        self.ipn_url = None
        self.payment_reciever = None
    