# from django import forms
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, HTML, Field, Fieldset, ButtonHolder, Submit
# from crispy_forms.bootstrap import FieldWithButtons, StrictButton
# from mailchimp import utils
# from mailchimp.chimpy.chimpy import ChimpyException
#
# from mezzanine.conf import settings
#
# from mezzcms.blog.models import BlogPost, BlogCategory
# from subscription.models import Subscriber
# from subscription.utils import subscribe_via_category
# from theme.models import Story
#
# SUBJECT_CHOICES = (
#     ('this','This'),
#     ('that','That'),
#     ('other','The Other'),
# )
#
#
# class SubscribeForm(forms.Form):
#     email = forms.EmailField(
#         label='Email',
#         widget=forms.TextInput(
#             {"type": "email", "placeholder": "Enter your email"}),
#     )
#
#     def __init__(self, *args, **kwargs):
#
#         url = "/subscribe/"
#         category_slug = kwargs.pop('category_slug', None)
#         if category_slug:
#             url = '/subscribe/c/{}/'.format(category_slug)
#
#         story_slug = kwargs.pop('story_slug', None)
#         if story_slug:
#             url = '/subscribe/s/{}/'.format(story_slug)
#
#         article_slug = kwargs.pop('article_slug', None)
#         if article_slug:
#             url = '/subscribe/a/{}/'.format(article_slug)
#
#         print "subscribe url: {}".format(url)
#
#         super(SubscribeForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-subscribe-form'
#         self.helper.form_action = ''.join(url)
#         # use ajax for all forms
#         self.helper.attrs = {'onsubmit': 'newsletter_ajax_submit(this);'}
#         # handled with javascript instead cause
#         # shortcode version doesn't work with csrf
#         self.helper.disable_csrf = True
#         self.helper.layout = Layout(
#             FieldWithButtons(
#                 'email', StrictButton("SUBMIT", type='submit')
#             )
#         )
#
#     def complete(self, type, slug, referrer):
#         """Create or update a Subscriber to have `gets_newsletter == True`.
#
#         If type is a (article), s (story), send the associated categories
#         If the type is c, senc the passed in category
#         if not type, then send no categories
#         """
#
#         email = self.cleaned_data['email']
#         email = email.lower()
#
#         subscriber, created = Subscriber.objects.get_or_create(
#             email=email, defaults={'gets_newsletter': True})
#
#         # If existing subscriber, update gets_newsletter
#         if not created:
#             subscriber.gets_newsletter = True
#             subscriber.save()
#
#         if type == 'a':
#             categories = set(BlogPost.objects.get(slug=slug).categories.all())
#         elif type == 's':
#             categories = set(Story.objects.get(slug=slug).categories.all())
#         elif type == 'c':
#             categories = set(BlogCategory.objects.get(slug=slug))
#         else:
#             categories = set()
#
#         subscribe_via_category(subscriber, categories, referrer)
#
#         return subscriber
#
#
# class FollowForm(forms.Form):
#     email = forms.EmailField(
#         label='',
#         widget=forms.TextInput({ "placeholder": "Enter your email"}),
#     )
#
#     def __init__(self, *args, **kwargs):
#         super(FollowForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-follow-form'
#         self.helper.layout = Layout(
#             FieldWithButtons(
#                 'email', StrictButton("SUBMIT", type='submit')
#             )
#         )
#
# class FollowFormExistingSubscriber(forms.Form):
#     subscriber_id = forms.CharField(label='', widget=forms.HiddenInput())
#
#     def __init__(self, *args, **kwargs):
#         super(FollowFormExistingSubscriber, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-follow-form'
#         self.helper.layout = Layout(
#             Fieldset(
#                 '',
#                 'subscriber_id',
#             ),
#             StrictButton("FOLLOW THIS", type='submit', css_class='btn-black'),
#         )
