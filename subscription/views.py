# from django.http import HttpResponseRedirect, Http404
# from django.core.urlresolvers import reverse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
#
# from mezzanine.utils.views import render
#
# from django.conf import settings
#
# from mezzcms.blog.models import BlogPost, BlogCategory
# from theme.models import Story
#
# from subscription.forms import (
#     SubscribeForm, FollowForm, FollowFormExistingSubscriber)
# from subscription.models import (
#     Subscriber, FollowStory, FollowArticle, FollowCategory)
# from subscription.utils import (
#     get_subcriber_id_from_cookie, get_referer_from_request,
#     subscribe_via_article, unsubscribe_from_mail_chimp, subscribe_via_stories)
#
# # -----------------------------------------------------------------------------
# #   :: Subscribe
# # -----------------------------------------------------------------------------
#
#
# # @csrf_exempt
# def subscribe(
#         request, type=None, slug=None, template='subscription/subscribe.html'):
#     """View method for all incoming subscribe requests.
#
#     This method doesn't not create a form.  See SubscribeForm.
#
#     If article or story in context, subscribe to related categories.
#     If article is News Analysis, add news analysis to list of categories
#     If category in context, subscribe to it
#     If nothing is in context, just subscribe without category.
#     """
#
#     if type == 'a':
#         subscribe_form = SubscribeForm(request.POST or None, article_slug=slug)
#     elif type == 's':
#         subscribe_form = SubscribeForm(request.POST or None, story_slug=slug)
#     elif type == 'c':
#         subscribe_form = SubscribeForm(request.POST or None, category_slug=slug)
#     else:
#         subscribe_form = SubscribeForm(request.POST or None)
#
#     referrer = request.META.get('HTTP_REFERER', "")
#
#     if subscribe_form.is_valid():
#         subscriber = subscribe_form.complete(type, slug, referrer)
#         response = HttpResponseRedirect(reverse('subscribe_thank_you'))
#         response.set_cookie('is_subscriber', subscriber.id)
#         return response
#
#     context = {
#         'subscribe': subscribe_form,
#     }
#
#     return render(request, template, context)
#
#
# # @csrf_exempt
# def subscribe_thank_you(request, template='subscription/subscribe_thank_you.html'):
#
#     more_stories = BlogPost.objects.filter(status=2).order_by('rating', 'publish_date')[:3]
#
#     context = {
#         'more_stories': more_stories,
#     }
#
#     return render(request, template, context)
#
#
# #-------------------------------------------------------------------------------
# #   :: Follow Page / Follow External
# #-------------------------------------------------------------------------------
#
# def follow_form(request, template="subscription/follow_form.html"):
#
#     """
#     Form page view to capture an External follow link from 3rd party source.
#
#     If request is to follow an Article, first see if it is in any stories.
#     If so, follow the articles' stories instead.
#     Fallback to following the article when not in any stories.
#     """
#
#     # Get parameters
#     follow_type = request.GET.get('type', False)
#     follow_id = request.GET.get('id', False)
#     follow_referrer = request.GET.get('ref', False)
#
#     # TODO validate that the GET parameters exist, and handle errors if so
#     if not follow_type and not follow_id:
#         raise Http404
#
#     follow_title = '' # display title of the Follow object
#     follow_obj = None # the Follow object
#     follow_stories = []  # may be populated with stories that contain an article
#
#     # Get content to Follow
#     if follow_type == 'article':
#         try:
#             follow_obj = BlogPost.objects.get(id=follow_id)
#             follow_title = follow_obj.title
#             follow_stories = follow_obj.get_parent_stories()
#         except BlogPost.DoesNotExist:
#             # TODO: What to do with missing follow objects?
#             raise Http404
#     elif follow_type == 'story':
#         try:
#             follow_obj = Story.objects.get(id=follow_id)
#             follow_title = follow_obj.title
#         except Story.DoesNotExist:
#             # TODO: What to do with missing follow objects?
#             raise Http404
#     elif follow_type == 'category':
#         try:
#             follow_obj = BlogCategory.objects.get(id=follow_id)
#             follow_title = follow_obj.title
#         except BlogCategory.DoesNotExist:
#             # TODO: What to do with missing follow objects?
#             raise Http404
#
#     # Check for subscriber cookie
#     subscriber = False
#     email = False
#
#     subscriber_id = get_subcriber_id_from_cookie(request) # subscription.utils
#     try:
#         subscriber = Subscriber.objects.get(id=subscriber_id)
#         email = subscriber.email
#     except Subscriber.DoesNotExist:
#         # No need to do anything, subscriber will be created and cookie
#         # added. And email will be captured.
#         pass
#
#     # Add follow content to Subcriber, else give "already following"
#     is_following = False
#     if subscriber:
#         if follow_type == 'article':
#             if follow_stories:
#                 #  article contained in stories, add the stories instead
#                 existing_follow_objs = []
#                 for story in follow_stories:
#                     try:
#                         existing_follow_objs.append(FollowStory.objects.get(
#                             story=story, subscriber=subscriber).follow_story)
#                     except FollowStory.DoesNotExist:
#                         pass
#                 is_following = any(existing_follow_objs)
#             else:
#                 #  Stand alone article, not in any stories
#                 try:
#                     existing_follow_obj = FollowArticle.objects.get(
#                         article=follow_obj, subscriber=subscriber).follow_story
#                 except FollowArticle.DoesNotExist:
#                     pass
#         elif follow_type == 'story':
#             try:
#                 existing_follow_obj = FollowStory.objects.get(
#                     story=follow_obj, subscriber=subscriber).follow_story
#             except FollowStory.DoesNotExist:
#                 pass
#         elif follow_type == 'category':
#             try:
#                 is_following = FollowCategory.objects.get(
#                     category=follow_obj, subscriber=subscriber).follow_story
#             except FollowCategory.DoesNotExist:
#                 pass
#
#     # Form stuffs
#     if subscriber:
#         initial = {'subscriber_id': subscriber.id}
#         form = FollowFormExistingSubscriber(
#             request.POST or None, initial=initial)
#     else:
#         form = FollowForm(request.POST or None)
#
#     if form.is_valid():
#         # Form for existing Subscriber
#         if form.__class__ == FollowFormExistingSubscriber:
#             subscriber_id = form.cleaned_data['subscriber_id']
#             subscriber = Subscriber.objects.get(id=subscriber_id)
#         # Form for new Subscriber
#         elif form.__class__ == FollowForm:
#             # Get or create the subscriber
#             email = form.cleaned_data['email']
#             email = email.lower()
#             subscriber, created = Subscriber.objects.get_or_create(email=email)
#
#         # Create follow_detail on through model
#         followed_objs = []
#         if follow_type == 'article':
#             if follow_stories:
#                 followed_objs = subscribe_via_stories(
#                     follow_stories, subscriber)
#             else:
#                 #  A stand-alone article, not in any stories
#                 followed_objs.append(
#                     subscribe_via_article(follow_obj, subscriber))
#
#         elif follow_type == 'story':
#             followed_objs = subscribe_via_stories([follow_obj], subscriber)
#
#         elif follow_type == 'category':
#             follow_category, created = FollowCategory.objects.get_or_create(
#                 category=follow_obj, subscriber=subscriber)
#             followed_objs.append(follow_category)
#
#         # pass subscriber id to follow_thank_you
#         url = reverse('follow_thank_you', kwargs={'pk': subscriber.id})
#         if follow_type:
#             url = '{0}?type={1}'.format(url, follow_type)
#         return HttpResponseRedirect(url)
#
#     context = {
#         'form': form,
#         'follow_title': follow_title,
#         'follow_obj': follow_obj,
#         'follow_type': follow_type,
#         'is_following': is_following,
#         'subscriber': subscriber,
#         'email': email,
#     }
#
#     return render(request, template, context)
#
#
# def follow_thank_you(request, pk=None, template='subscription/follow_thank_you.html'):
#
#     """
#     Thank you page for after follow and article.
#         @pk = Subscriber ID
#     """
#
#     follow_type = request.GET.get('type', False)
#
#     if pk is None:
#         raise Http404
#
#     if not request.COOKIES.has_key('is_subscriber'):
#         url = reverse('follow_thank_you', kwargs={'pk': pk})
#         if follow_type:
#             url = '{0}?type={1}'.format(url, follow_type)
#         response = HttpResponseRedirect(url)
#         response.set_cookie('is_subscriber', pk)
#         return response
#     else:
#         pass
#
#     more_stories = BlogPost.objects.filter(status=2).order_by('rating', 'publish_date')[:3]
#
#     context = {
#         'follow_type': follow_type,
#         'more_stories': more_stories,
#     }
#
#     return render(request, template, context)
#
# #-------------------------------------------------------------------------------
# #   :: Unfollow
# #-------------------------------------------------------------------------------
#
# def unfollow(request, template="subscription/unfollow_thank_you.html"):
#
#     # Get parameters
#     follow_type = request.GET.get('type', False)
#     follow_id = request.GET.get('id', False)
#
#     # TODO validate that the GET parameters exist, and handle errors if so
#     if not follow_type and not follow_id:
#         raise Http404
#
#     # Check for subscriber cookie
#     subscriber = False
#     subscriber_id = get_subcriber_id_from_cookie(request) # subscription.utils
#     try:
#         subscriber = Subscriber.objects.get(id=subscriber_id)
#     except:
#         #TODO: what to do with no user
#         raise Http404
#
#     # Get object
#     follow_obj = None
#     followed_objs = []
#     if follow_type == 'article':
#         try:
#             follow_obj = BlogPost.objects.get(id=follow_id)
#         except BlogPost.DoesNotExist:
#             # TODO: What to do with missing follow objects?
#             raise Http404
#     elif follow_type == 'story':
#         try:
#             follow_obj = Story.objects.get(id=follow_id)
#         except Story.DoesNotExist:
#             # TODO: What to do with missing follow objects?
#             raise Http404
#     elif follow_type == 'category':
#         try:
#             follow_obj = BlogCategory.objects.get(id=follow_id)
#         except BlogCategory.DoesNotExist:
#             # TODO: What to do with missing follow objects?
#             raise Http404
#
#     # unfollow the object
#     if follow_type == 'article':
#         #  If the article is one or more stories, then follow the stories
#         #  otherwise, just follow the article.
#         stories = follow_obj.get_parent_stories()
#         if stories:
#             for story in stories:
#                 followed_objs.append(FollowStory.objects.get(
#                     story=story, subscriber=subscriber))
#         else:
#             followed_objs.append(FollowArticle.objects.get(
#                 article=follow_obj, subscriber=subscriber))
#
#     elif follow_type == 'story':
#         followed_objs.append(FollowStory.objects.get(
#             story=follow_obj, subscriber=subscriber))
#
#     elif follow_type == 'category':
#         followed_objs.append(FollowCategory.objects.get(
#             category=follow_obj, subscriber=subscriber))
#
#     unsubscribe_from_mail_chimp(subscriber)
#
#     for follow in followed_objs:
#         follow.follow_story = False
#         follow.save()
#
#     context = {
#         'follow_type': follow_type,
#     }
#
#     return render(request, template, context)
#
# #-------------------------------------------------------------------------------
# #   :: External Follow Link Button
# #-------------------------------------------------------------------------------
#
# def external_follow_link_button(request, template='subscription/external_follow_link_button.html'):
#
#     """
#     View to generate a simple Follow <a> linking backe to the Follow view form.
#
#     Used as an <iframe> on third party sites.
#     """
#
#     pre_text = 'Story by CALmatters. Click to'
#     link_text = 'Follow This Story'
#
#     follow_type = request.GET.get('type', False)
#     follow_id = request.GET.get('id', False)
#
#     if request.GET.get('pre', False):
#         pre_text = request.GET.get('pre', False)
#
#     if request.GET.get('text', False):
#         link_text = request.GET.get('text', False)
#
#     try:
#         referer = request.META['HTTP_REFERER']
#         referer = get_referer_from_request(referer)
#         referer = '&ref={0}'.format(referer)
#     except:
#         print 'except'
#         referer = ''
#
#     form_page = reverse('subscription_follow_form')
#
#     follow_url = '{0}?type={1}&id={2}{3}'.format(form_page, follow_type,
#                                                  follow_id, referer)
#
#     context = {
#         'pre_text': pre_text,
#         'link_text': link_text,
#         'follow_url': follow_url,
#     }
#
#     return render(request, template, context)
#
# #-------------------------------------------------------------------------------
# #   :: External Follow Generator
# #-------------------------------------------------------------------------------
#
# @login_required
# def external_follow_generator(request, template='subscription/external_follow_generator.html'):
#
#     """
#     Generate an embed code for a third party to use as an Exteranal follow link.
#     """
#
#     article_list = BlogPost.objects.all().values()
#     story_list = Story.published.all().values()
#     category_list = BlogCategory.objects.all().values()
#
#     context = {
#         'site_url_root': settings.SITE_URL_ROOT,
#         'article_list': article_list,
#         'story_list': story_list,
#         'category_list': category_list,
#     }
#
#     return render(request, template, context)
