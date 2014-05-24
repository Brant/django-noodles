"""
Utility functions for the Noodly Ecommerce module
"""


def generate_ipn_postback_data(postdata):
    """
    Paypal sends a bunch of post stuff and wants us to send it back
    
    Returned data needs to be in a particular format
    
    This generates that data string
    
    'postdata' is essentially a dict
    """
    url_data = "cmd=_notify-validate"
    
    for key in postdata:
        url_data += "&%s=%s" % (key, postdata[key])
        
    return url_data