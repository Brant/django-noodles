"""
Models for Noodly E-Commerce
"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class PayPalMetaTemplate(models.Model):
    """
    Metadata for where the IPN url is and what receiver email it should register
    """

    ipn_url = models.CharField(max_length=1000)
    reciever_email = models.EmailField(max_length=300)
    active = models.BooleanField(default=False, help_text="Only 1 meta handler can be active at a time")

    def save(self, *args, **kwargs):
        """
        Custom save, allowing only 1 active at a time
        """

        super(PayPalMetaTemplate, self).save(*args, **kwargs)

        if self.active:
            metas = self.__class__.objects.filter(~models.Q(pk=self.id), active=True)
            for meta in metas:
                meta.active = False
                meta.save()

    class Meta:
        """
        Django Metadata
        """
        abstract = True
        verbose_name = "PayPal Metadata"
        verbose_name_plural = "PayPal Metadata"


class PayPalPayment(models.Model):
    """
    Represents a paypal payment's important data, returned from PayPal IPN
    """
    invoice = models.CharField(max_length=100)
    transaction = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)

    shipping_name = models.CharField(max_length=300, null=True, blank=True)
    street = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)

    def __unicode__(self):
        return self.invoice

    class Meta:
        """
        Django metadata
        """
        ordering = ["-date"]


class PayPalPurchasable(models.Model):
    """
    Abstract base class for creating a purchasable item
    """
    payment = models.OneToOneField(PayPalPayment, null=True, blank=True, editable=False)
    
    def paid(self):
        """
        Has this purchase been paid for
        """
        if self.payment:
            return True
        return False

    class Meta:
        """
        Django metadata
        """
        abstract = True

    def get_payment(self):
        """
        Get corresponding paypal payment
        """
        try:
            return self.payment
        except ObjectDoesNotExist:
            return None
