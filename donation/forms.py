from django import forms
from django.core.exceptions import ValidationError


class StripeCustomerForm(forms.Form):
    
    AMOUNT_CHOICES = [
        ('100','$100'),
        ('250','$250'),
        ('1000','$1000'),
        ('0','Other'),
    ]
         
    stripe_token        = forms.CharField()
    stripe_email        = forms.EmailField(label="EMAIL")
    stripe_amount       = forms.ChoiceField(label="AMOUNT",choices=AMOUNT_CHOICES,widget=forms.RadioSelect(),required=False)
    stripe_amount_other = forms.IntegerField(label="OR OTHER AMOUNT",required=False)
    
    first_name          = forms.CharField(label="FIRST NAME")
    last_name           = forms.CharField(label="LAST NAME")
    phone               = forms.CharField(label="PHONE")
    address1            = forms.CharField(label="ADDRESS 1")
    address2            = forms.CharField(label="ADDRESS 2",required=False)
    city                = forms.CharField(label="CITY")
    state               = forms.CharField(label="STATE")
    zip_code            = forms.CharField(label="ZIP")
    
    card                = forms.CharField(label="CARD NUMBER")
    exp_month           = forms.IntegerField(label="MONTH [MM]")
    exp_year            = forms.IntegerField(label="YEAR [YYY]")
    cvc                 = forms.IntegerField(label="CVC")
    
    sub_newsletter      = forms.BooleanField(label='Subscribe to newsletter',required=False)

