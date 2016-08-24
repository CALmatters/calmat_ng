from django.contrib.sitemaps import Sitemap

from pages.models import Article



class NewsSitemap(Sitemap):
    """To be use with Google News to index CALmatters news through a sitemap"""

    changefreq = 'daily'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Article.objects.published()

    def lastmod(self, obj):
        return obj.publish_date
