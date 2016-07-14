import logging
from django.conf import settings

import mailchimp

logger = logging.getLogger(__name__)


def get_api():
    return mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)


# def get_list():
#     return get_api().lists.list(filters={'id': settings.MAILCHIMP_MAIN_LIST_ID})
#
#     all_members = api.lists.members(settings.MAILCHIMP_MAIN_LIST_ID)


def get_subscriber_record(email):
    """The MailChimp record for the email.

    If not found, None is returned.
    Other errors are written to log
    """

    member = get_api().lists.member_info(
        settings.MAILCHIMP_MAIN_LIST_ID, [{'email': email}, ])
    if member['errors']:
        if any(err for err in member['errors'] if err['code'] == 232):
            # Member doesn't exist yet
            logger.info("{} doesn't exist yet, will create in MC".format(email))
        else:
            logger.warn("Error from MC:  {}".format(member['errors']))

        return None

    else:
        return member['data'][0]


def get_current_category_subscriptions(email):
    """Should return

    ['Transportation']

    if selections are

    [{'interested': False, 'name': 'Cap and Trade'},
     {'interested': False, 'name': 'Climate Change'},
     {'interested': False, 'name': 'Poverty'},
     {'interested': False, 'name': 'Environment'},
     {'interested': False, 'name': 'News Analysis'},
     {'interested': False, 'name': 'Personalities'},
     {'interested': False, 'name': 'Politics'},
     {'interested': True, 'name': 'Transportation'}]
    """

    member = get_subscriber_record(email)

    if member:
        return set(
            b['name'] for b in
            next(iter(
                [g for g in member['merges']['GROUPINGS']
                 if g['id'] == settings.MAILCHIMP_GROUPING_ID]))['groups']
            if b['interested'])
    else:
        return set()


def subscribe_to_mail_chimp(email, categories=()):
    """Add a email and categories of interest to the main mailing list

    Adds or updates a subscriber.
    Associate categories, as Interest Groups, to subscriber

    https://github.com/piquadrat/django-mailchimp
    """

    print("Using MC API_KEY:  {}".format(settings.MAILCHIMP_API_KEY))
    print("Using MC LIST ID:  {}".format(settings.MAILCHIMP_MAIN_LIST_ID))

    existing_categories = get_current_category_subscriptions(email)

    #  Convert Category objects to a list of names
    new_categories = set(
        cat.title.strip() for cat in categories if cat.title.strip())

    categories = existing_categories | new_categories

    # print("existing")
    # print(existing_categories)
    # print("new")
    # print(new_categories)
    # print("to save")
    # print(categories)

    merge_vars = dict(
        groupings=[dict(
            id=settings.MAILCHIMP_GROUPING_ID,
            groups=list(categories))])


    try:
        kwargs = dict(
            id=settings.MAILCHIMP_MAIN_LIST_ID,
            email={'email': email},
            update_existing=True,
            replace_interests=True,
            merge_vars=merge_vars)
        logger.info(kwargs)
        get_api().lists.subscribe(**kwargs)
    except mailchimp.ListInvalidInterestGroupError:
        logger.warn(
            "Unknown category in {}.  Probably added in CALmatters, "
            "but not in MC".format(categories))
