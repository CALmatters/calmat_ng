from django.db import models

from media_manager.models import MediaItem
from sites.models import TimeStamped, Publishable

class Testimonial(Publishable, TimeStamped):
    
    """
    This model is for testimonials on the donate page.
    """
    
    full_name = models.CharField('Full Name',max_length=150)
    job_title = models.CharField('Job Title',max_length=150)

    testimonial_image = models.ForeignKey(
        MediaItem,
        verbose_name="Testimonial Image",
        null=True,
        blank=True,
        related_name="testimonial_image")

    message = models.TextField(verbose_name='Testimonial Message')

    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['order','full_name']
        get_latest_by = 'created'