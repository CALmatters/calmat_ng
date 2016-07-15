from django.db import models

from sites.models import Named, ContentContainer, Publishable, TimeStamped


class JobListing(Named, Publishable, ContentContainer, TimeStamped):
    """Individual job to be displayed on site"""

    def get_absolute_url(self):
        return "/job/{}/".format(self.slug)


    class Meta:
        verbose_name = "Job Listing"
        verbose_name_plural = "Job Listings"


class RelatedJobListings(models.Model):

    job_title = models.ForeignKey("employment.JobPage", related_name='titles_for_rel')
    job_listing = models.ForeignKey(
        JobListing, related_name='listings_for_rel')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return u''

    class Meta:
        verbose_name = "Related Job Listing"
        verbose_name_plural = "Related Job Listings"
        ordering = ('order', )


class JobPage(Named, ContentContainer, TimeStamped):
    """Landing page information aggregating all listings"""

    job_listings = models.ManyToManyField(
        JobListing, through=RelatedJobListings)

    def get_absolute_url(self):
        return "/jobs/{}/".format(self.slug)

    class Meta:
        verbose_name = "Job Page"
        verbose_name_plural = "Job Pages"
