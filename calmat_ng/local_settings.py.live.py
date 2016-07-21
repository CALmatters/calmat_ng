DEBUG = False
ALLOWED_HOSTS = ('ng.calmatters.org', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'calmat_ng',
        'USER': 'calmatters',
        'PASSWORD': 'calmatters_db1',
        'HOST': 'localhost',
    }
}

SEND_SUBSCRIPTIONS_TO_MAIL_CHIMP = True

MAILCHIMP_API_KEY = '3a8ed455e09e98a38499fb79e00c781c-us11'
MAILCHIMP_MAIN_LIST_ID = '2df804b292'

# MAILCHIMP_API_KEY = 'bbd4a11d712364e23fee69e0b89e63a6-us11'  #  CALMat acct
# MAILCHIMP_MAIN_LIST_ID = 'faa7be558d'  #  Main List CALMatters

# live Stripe API Keys for CALmatters
STRIPE_PUBLIC_KEY = 'pk_live_Yq6s9UTUS4jPAFC2M0A3OxO5'
STRIPE_SECRET_KEY = 'sk_live_UvlyLbiquDqE97n8vuYgCMnj'
