import stripe
from django.contrib import messages
from django.conf import settings


def delete_stripe_customer(sender, **kwargs):
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    # retrieve the object instance from the keyword arguments.
    customer = kwargs['instance']
    
    # delete the customer from stripe
    stripe_customer = stripe.Customer.retrieve(customer.stripe_id)
    stripe_customer.delete()
    
