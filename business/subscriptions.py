# import logging
# from django.conf import settings
#
# from mailchimp import utils
#
# logger = logging.getLogger(__name__)
#
# def subscribe_to_mail_chimp(email, categories=()):
#     """Add a email and categories of interest to the main mailing list
#
#     Adds or updates a subscriber.
#     Associate categories, as Interest Groups, to subscriber
#
#     https://github.com/piquadrat/django-mailchimp
#     """
#
#     print("Using MC API_KEY:  {}".format(settings.MAILCHIMP_API_KEY))
#     print("Using MC LIST ID:  {}".format(settings.MAILCHIMP_MAIN_LIST_ID))
#
#     mc_list = utils.get_connection().get_list_by_id(
#         settings.MAILCHIMP_MAIN_LIST_ID)
#
#     member = utils.get_connection().con.list_member_info(
#         settings.MAILCHIMP_MAIN_LIST_ID, email)
#
#     interest_group = None
#     for group in utils.get_connection().con.list_interest_groupings(
#             settings.MAILCHIMP_MAIN_LIST_ID):
#         if group[u'name'] == settings.MAILCHIMP_GROUPING_NAME:
#             interest_group = group
#
#     group_titles_set = set(utils.get_connection().con.list_interest_groups(
#         settings.MAILCHIMP_MAIN_LIST_ID, interest_group['id']))
#
#     logger.debug("*********** group_titles_set ***********")
#     logger.debug(group_titles_set)
#
#     error_response = u'The email address passed does not exist on this list'
#     if 'error' in member.keys() and member['error'] == error_response:
#         #  subscriber doesn't exist yet
#         logger.warn("Error from MC:  {}".format(member['error']))
#         member_group_titles_set = set()
#     else:
#         #  subscriber exists, so merge new cats with existing ones
#         groupings = member['merges']['GROUPINGS']
#         interest_group = next(
#             group for group in groupings
#             if group[u'name'] == settings.MAILCHIMP_GROUPING_NAME)
#
#         logger.debug("*********** init member_group_titles_set ***********")
#         logger.debug(interest_group['groups'])
#
#         member_group_titles_set = map(
#             unicode.strip, interest_group['groups'].split(','))
#         member_group_titles_set = set(
#             (title for title in member_group_titles_set if title))
#
#     new_group_titles_set = set(
#         (cat.title.strip() for cat in categories if cat.title.strip()))
#
#     new_member_titles_set = new_group_titles_set | member_group_titles_set
#     titles_to_create_set = new_member_titles_set - group_titles_set
#
#     logger.debug("*********** new_member_titles_set ***********")
#     logger.debug(new_member_titles_set)
#
#     logger.debug("*********** titles_to_create_set ***********")
#     logger.debug(titles_to_create_set)
#
#     grouping_id = interest_group['id']
#     for group_title in titles_to_create_set:
#         logger.debug(
#             "Adding new group:  {} to {}".format(group_title, grouping_id))
#         try:
#             mc_list.add_interest_group(
#                 group_title, grouping_id=grouping_id)
#         except ChimpyException, e:
#             if "Oops! Group names need to be unique." not in e.message:
#                 raise
#
#     merge_vars = dict(
#         GROUPINGS=[dict(
#             name=settings.MAILCHIMP_GROUPING_NAME,
#             groups=', '.join(new_member_titles_set))])
#
#     logger.debug(mc_list.subscribe(
#         subscriber_email, update_existing=True, merge_vars=merge_vars))
