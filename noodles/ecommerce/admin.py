"""
Admin Panel options for Noodly Ecommerce
"""
from django.contrib import admin

from noodles.ecommerce.models import PayPalPayment


class PayPalMetaAdmin(admin.ModelAdmin):
    """
    Paypal Metadat Admin Configuration
    """
    list_display = ['pk', 'ipn_url', 'reciever_email', 'active']
    list_display_links = ['ipn_url', ]


class PayPalPaymentAdmin(admin.ModelAdmin):
    list_display = ["email", "invoice", ]


admin.site.register(PayPalPayment, PayPalPaymentAdmin)