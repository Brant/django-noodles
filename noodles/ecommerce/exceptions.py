"""
Custom exceptions
"""

class PayPalError(Exception):
    """
    Exception for paypal problems
    """
    pass


class PayPalAlreadyPaidError(PayPalError):
    """
    Exception when a transaction has already been paid for
    """
    pass


class PayPalMissingValueError(PayPalError):
    """
    Exception for missing data from paypal's IPN Post
    """
    pass


class PayPalRecieverError(PayPalError):
    """
    Exception for Wrong Reciever Email Address
    """
    pass


class PayPalUnverified(PayPalError):
    """
    Exception for an Unverified response from paypal
    """
    pass


class PayPalGrossTotalError(PayPalError):
    """
    Exception for Wrong Gross Total
    """
    pass


class UnimplementedPaypalListenerMethod(NotImplementedError):
    """
    Exception for unimplemented methods in PayPalListener
    """
    pass