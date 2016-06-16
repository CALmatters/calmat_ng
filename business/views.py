import logging

from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

# from business.subscriptions import subscribe_to_mail_chimp

logger = logging.getLogger(__name__)


@csrf_exempt
def subscribe(request):
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
            # subscribe_to_mail_chimp(email, categories)
        else:
            logger.debug(
                "skippping subscribing {} with {}".format(
                    email, len(categories)))
    else:
        raise PermissionDenied

    return redirect(request.META.get('HTTP_REFERER', '/'))
