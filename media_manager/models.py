import PIL
from PIL.Image import Image
from django.db import models

from versatileimagefield.fields import VersatileImageField

from django.conf import settings

IMAGE_TYPE_CHOICES = (
    ('photo', 'photo'),
    ('illustration', 'illustration'),
    ('graphic', 'graphic'))

LICENSE_CHOICES = (
    ('calmatters owned', 'CALmatters owned',),
    ('licensed', 'Licensed', ),
    ('creative commons', 'Creative Commons', ),
)


class MediaSource(models.Model):

    class Meta:
        verbose_name = "Media Source"
        verbose_name_plural = "Media Sources"

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def resize_image(image_path):
    """Given a local image file, downsize the image, if necessary"""

    with PIL.Image.open(image_path) as im:
        if im.size[0] > settings.IMAGES_UPLOADED_MAX_WIDTH_PX:

            ratio = float(
                settings.IMAGES_UPLOADED_MAX_WIDTH_PX) / float(im.size[0])
            new_height = int(ratio * float(im.size[1]))
            print("Resizing Image: %s, %s, %s " % (
                image_path, settings.IMAGES_UPLOADED_MAX_WIDTH_PX, new_height))
            new_image = im.resize(
                (settings.IMAGES_UPLOADED_MAX_WIDTH_PX, new_height),
                PIL.Image.ANTIALIAS)
            new_image.save(image_path, im.format)


class MediaItem(models.Model):
    """Each uploaded media file is references/wrapped by this this Media class

    This class defines the metadata to track for each file uploaded.
    """

    class Meta:
        verbose_name = "Media Item"
        verbose_name_plural = "Media Items"

    source = models.ForeignKey(MediaSource, null=True)
    creator = models.CharField(
        max_length=255,
        verbose_name="Photographer / creator",
        blank=True,
        null=True)
    image_type = models.CharField(
        max_length=30,
        choices=IMAGE_TYPE_CHOICES,
        blank=True,
        null=True)
    license = models.CharField(
        max_length=30,
        choices=LICENSE_CHOICES,
        blank=True,
        null=True)
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    alt_tag = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    date = models.DateField(
        verbose_name="Date taken",
        null=True,
        blank=True)

    file = VersatileImageField(upload_to="uploads/")

    def save(self, **kwargs):
        super(MediaItem, self).save(**kwargs)

        resize_image(self.file.path)

    def __str__(self):
        return self.caption[:20]
