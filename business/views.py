import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

# from business.subscriptions import subscribe_to_mail_chimp
from business.subscriptions import subscribe_to_mail_chimp
from pages.models import Article, Project

logger = logging.getLogger(__name__)


@csrf_exempt
def subscribe(request, template="subscription/subscribe.html"):
    """Email address from POST is sent to MailChimp"""

    if request.method == 'POST':
        email = request.POST.get('email', None)
        email = email.lower()
        print(email)

        # Todo: Capture categories
        categories = ()

        if settings.SEND_SUBSCRIPTIONS_TO_MAIL_CHIMP:
            logger.debug(
                "subscribing {} with {} categories".format(
                    email, len(categories)))
            subscribe_to_mail_chimp(email, categories)
        else:
            logger.debug(
                "skippping subscribing {} with {}".format(
                    email, len(categories)))
        template = "subscription/subscribe_thank_you.html"

        context = dict(
            more_stories=Article.objects.published().filter(
                image__isnull=False).order_by('publish_date')[:3])

        return render(request, template, context)
    else:
        return render(request, template, context={})


