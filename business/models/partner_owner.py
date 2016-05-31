from sites.models import Named, TimeStamped


class PartnerOwner(Named, TimeStamped):

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        ordering = ("title",)

    def get_absolute_url(self):
        name = self.__class__.__name__
        raise NotImplementedError("The model %s does not have "
                                  "get_absolute_url defined" % name)
