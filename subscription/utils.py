# from django.core.exceptions import ObjectDoesNotExist
# from mailchimp import utils
# from django.conf import settings
# from mailchimp.chimpy.chimpy import ChimpyException
#
# from mezzcms.blog.models import BlogPost, BlogCategory
# from theme.models.stories import Story
# from subscription.models import Subscriber, FollowArticle, FollowStory, FollowCategory
# from mezzcms.utils import *
#
#
# import logging
#
# logger = logging.getLogger(__name__)
#
# def get_subcriber_id_from_cookie(request):
#
#     """
#     Return the value of the cookie `is_subscriber` if it exists.
#     Else, return False.
#     """
#
#     # Test for `is_subscriber` cookie first
#     if request.COOKIES.has_key('is_subscriber'):
#         subscriber_id = request.COOKIES['is_subscriber']
#
#         if Subscriber.objects.filter(id=subscriber_id).exists():
#             return subscriber_id
#         else:
#             return False
#     else:
#         return False
#
#
# def gets_newsletter(request):
#
#     subscriber_id = get_subcriber_id_from_cookie(request)
#
#     try:
#         subscriber = Subscriber.objects.get(id=subscriber_id)
#     except:
#         return False
#
#     return subscriber.gets_newsletter
#
#
# def subscriber_is_following(request, follow_type, object_id):
#
#     """
#     See if the current user is following this `follow_type` with `object_id`.
#
#     Return False when:
#         - not a subscriber cookie
#         - not a Subscriber object for cookie ID value
#         - follow_object for `follow_type` and `object_id` does not exist
#         - the Subscriber is not following the content
#         (no Follow* through table entry)
#
#     Otherwise, return the boolean value of the through model `is_following`.
#     """
#
#     subscriber_id = get_subcriber_id_from_cookie(request)
#     try:
#         subscriber = Subscriber.objects.get(id=subscriber_id)
#     except:
#         return False
#
#     follow = None
#     # Get content Follow
#     if follow_type == 'article':
#         try:
#             follow_obj = BlogPost.objects.get(id=object_id)
#             stories = follow_obj.get_parent_stories()
#             if stories:
#                 for story in stories:
#                     try:
#                         if FollowStory.objects.get(
#                                 story=story,
#                                 subscriber=subscriber).follow_story:
#                             return True
#                     except FollowStory.DoesNotExist:
#                         pass
#             else:
#                 follow = FollowArticle.objects.get(
#                     article=follow_obj, subscriber=subscriber)
#         except ObjectDoesNotExist:
#             return False
#     elif follow_type == 'story':
#         try:
#             follow_obj = Story.objects.get(id=object_id)
#             follow = FollowStory.objects.get(story=follow_obj, subscriber=subscriber)
#         except ObjectDoesNotExist:
#             return False
#     elif follow_type == 'category':
#         try:
#             follow_obj = BlogCategory.objects.get(id=object_id)
#             follow = FollowCategory.objects.get(category=follow_obj, subscriber=subscriber)
#         except ObjectDoesNotExist:
#             return False
#
#     if follow:
#         return follow.follow_story
#     else:
#         return False
#
#
# def get_referer_from_request(http_referer):
#
#     """
#     Return the domain root from a request.META.HTTP_REFERER @http_referer
#     """
#
#     regex = re.compile('https?://([a-zA-Z0-9.]+)')
#
#     referer = regex.match(http_referer)
#
#     if referer:
#         return referer.group(1)  # get the () regex capture
#     else:
#         return False
#
#
# def subscribe_to_mail_chimp(subscriber_email, categories=set()):
#     """Add a subscriber to the main Calmatters mailing list with groups
#
#     Adds or updates a subscriber.
#     Associate categories, as Interest Groups, to subscriber
#
#     https://github.com/piquadrat/django-mailchimp
#     """
#
#     print "Using MC API_KEY:  {}".format(settings.MAILCHIMP_API_KEY)
#     print "Using MC LIST ID:  {}".format(settings.MAILCHIMP_MAIN_LIST_ID)
#
#     mc_list = utils.get_connection().get_list_by_id(
#         settings.MAILCHIMP_MAIN_LIST_ID)
#
#     member = utils.get_connection().con.list_member_info(
#         settings.MAILCHIMP_MAIN_LIST_ID, subscriber_email)
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
#
#
# def unsubscribe_from_mail_chimp(subscriber):
#     """Set the email as unsubscribed at MC (not - not deleted) """
#
#     mc_list = utils.get_connection().get_list_by_id(
#         settings.MAILCHIMP_MAIN_LIST_ID)
#
#     mc_list.unsubscribe(subscriber.email)
#
#
# def subscribe_via_stories(stories, subscriber):
#     """Subscribe subscriber to follow stories
#
#     Only following Categories.  So, this method finds all the Categories
#     in the stories, follows them, and send them to MC
#     """
#
#     categories = []
#     for story in stories:
#         categories += [c for c in story.categories.all()]
#
#     #  Todo:  referrer could be passed in and not be just internal
#     return subscribe_via_category(subscriber, set(categories), 'internal')
#
#
# def subscribe_via_article(article, subscriber):
#     """Subscribe subscriber to follow articles
#
#     Only following Categories.  So, this method finds all the Categories
#     in the articles, follows them, and send them to MC
#     """
#
#     categories = [c for c in article.categories.all()]
#
#     # Todo:  referrer could be passed in and not be just internal
#     return subscribe_via_category(subscriber, set(categories), 'internal')
#
#
# def subscribe_via_category(subscriber, categories=set(), referrer=None):
#     """Subscribe subscriber to follow a category
#
#     The cateogry and subscriber are saved to the DB.  Then, regardless of
#     outcome, the mail and article title are saved to MailChimp.
#     """
#
#     if categories:
#         #  Todo:  do in a batch.
#         for category in set(categories):
#             follow_category, created = FollowCategory.objects.get_or_create(
#                 category=category,
#                 subscriber=subscriber,
#                 defaults=dict(
#                     follow_story=True,
#                     referrer='internal'))  # TODO: referrer would be nice
#
#     if settings.SEND_SUBSCRIPTIONS_TO_MAIL_CHIMP:
#         logger.debug("subscribing {} with {} categories".format(
#             subscriber.email, len(categories)))
#         subscribe_to_mail_chimp(subscriber.email, categories)
#     else:
#         logger.debug("skippping subscribing {} with {}".format(
#             subscriber.email, len(categories)))
#
#
