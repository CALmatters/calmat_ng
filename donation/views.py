import stripe
import mailchimp
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.template.loader import render_to_string


from .models import StripeCustomer
from .forms import StripeCustomerForm
from .mixins import StripeMixin

from pages.models import About

# TODO: import new Subscriber model to add to subscription -- MS 7.11.16
# from subscription.models import Subscriber

class DonationSuccessView(TemplateView):
    template_name = 'donation/donation_success.html'


class StripeCustomerView(StripeMixin, FormView):
    
    model = StripeCustomer
    template_name = 'donation/donation_form.html'
    form_class = StripeCustomerForm
    success_url = reverse_lazy('blog_views_support_us')
    
    def get_context_data(self, **kwargs):
        # return the amount and About to the context
        context = super(StripeCustomerView, self).get_context_data(**kwargs)
        context['about'] = About.objects.latest()
        if 'amount' in self.kwargs:
            context['amount'] = self.kwargs['amount']
        return context
    
    def create_stripe_charge(self):
        # create the Stripe charge. NEED BETTER ERROR HANDELING.
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe.Charge.create(
                amount = int(self.amount)*100, # in cents
                currency = "usd",
                customer = self.customer.id,
            )
            messages.info(self.request, 'Thank you for your donation of $%s to CALmatters.' % self.amount)
        except:
            messages.info(self.request, 'There was a problem processing your payment.')
    
    def subscribe_to_newsletter(self):

        # # TODO: create new Subscriber in new subscriber app -- MS 7.11.16
        # # subscribe to the CALmatters newsletter
        # subscriber, created = Subscriber.objects.get_or_create(email=self.email,
        #     defaults={'gets_newsletter': True})
        
        # # If existing subscriber, update gets_newsletter
        # if not created:
        #     subscriber.gets_newsletter = True
        #     subscriber.save()
        
        # Add subscriber to MailChimp list
        # https://github.com/piquadrat/django-mailchimp

        # TODO:  Dry this out to the subscription utils someday
        # TODO: add subscriber to MailChimp list subscribe_to_newsletter -- MS 7.11.16
        mc = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        mc_subscriber_type = 'mc_new_subscriber'
        mc_list = utils.get_connection().get_list_by_id(subscribe_to_newsletter)

        try:
            subcribed_to_list = mc_list.subscribe(self.email, {'EMAIL': self.email})
        except:
            # Email is already subscribed to list
            mc_subscriber_type = 'mc_old_subscriber'
            
        return True, subscriber, mc_subscriber_type
    
    def form_valid(self, form):
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        self.token = form.cleaned_data['stripe_token']
        self.email = form.cleaned_data['stripe_email']
        self.subscribe = form.cleaned_data['sub_newsletter']
        
        # get the amount to charge
        if form.cleaned_data['stripe_amount_other'] is not None:
            self.amount = form.cleaned_data['stripe_amount_other']
        else:
            self.amount = form.cleaned_data['stripe_amount']
        
        # subscribe to newsletter if checkbox checked
        if self.subscribe:
            pass
            # TODO: subscribe user to newsletter -- MS 7.11.16
            # self.subscribe_to_newsletter()
            
        # get or create the stripe customer
        cust, created = StripeCustomer.objects.get_or_create(
            stripe_email = self.email,
            defaults={    
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
                'address1': form.cleaned_data['address1'],
                'address2': form.cleaned_data['address2'],
                'city': form.cleaned_data['city'],
                'state': form.cleaned_data['state'],
                'zip_code': form.cleaned_data['zip_code'],
            }
        )
        if created:
            # if the object was created, create the Stripe customer
            self.customer = stripe.Customer.create(
                description = "Added via CALmatters",
                email = self.email,
                source = self.token
            )
            # add the Stripe customer to the local object
            cust.stripe_id = self.customer.id
            cust.save()
        else:
            # if not created, retrieve the Stripe customer
            self.customer = stripe.Customer.retrieve(cust.stripe_id)
        
        # create the stripe charge
        self.create_stripe_charge()
        
        return super(StripeCustomerView, self).form_valid(form)
    
