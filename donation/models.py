from __future__ import unicode_literals

import stripe
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete

from .signals import delete_stripe_customer


class StripeCustomer(models.Model):
    """
    
    """
    AMOUNT_CHOICES = [
        ('100','$100'),
        ('250','$250'),
        ('1000','$1000'),
        ('0','Other'),
    ]
    stripe_id = models.CharField('Stripe ID',max_length=140,blank=True,null=True)
    stripe_email = models.EmailField('email')
    
    first_name = models.CharField('first name',max_length=140)
    last_name = models.CharField('last name',max_length=140)
    phone = models.CharField('phone',max_length=140)
    address1 = models.CharField('address 1',max_length=140)
    address2 = models.CharField('address 2',max_length=140,blank=True,null=True)
    city = models.CharField('city',max_length=140)
    state = models.CharField('state',max_length=140)
    zip_code = models.CharField('zip code',max_length=10)
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("stripe customer")
        verbose_name_plural = _("stripe customers")
        get_latest_by = 'created'
    
    def __str__(self):
        return self.stripe_email
        
    def save(self, *args, **kwargs):
        super(StripeCustomer, self).save(*args, **kwargs)
    
    def full_name(self):
    	return u'%s %s' % (self.first_name,self.last_name)
    	
post_delete.connect(delete_stripe_customer, sender=StripeCustomer)