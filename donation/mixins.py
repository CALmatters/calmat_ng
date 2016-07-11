from django.conf import settings


class StripeMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        context['hidejs'] = True
        return context
