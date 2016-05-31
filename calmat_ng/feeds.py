from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed, Atom1Feed

from pages.models import Article


class ArticleFeed(Feed):
    title = "CALmatters site news"
    link = "/feeds/"
    description = "Updates on changes and additions to Calmatter's articles."

    def items(self):
        return Article.objects.order_by('-pub_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('articles', args=[item.pk])


class RssArticleFeed(ArticleFeed):
    feed_type = Rss201rev2Feed


class AtomArticleFeed(ArticleFeed):
    feed_type = Atom1Feed