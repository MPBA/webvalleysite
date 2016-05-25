from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import FileField


# # The members of Page will be inherited by the Author model, such
# # as title, slug, etc. For authors we can use the title field to
# # store the author's name. For our model definition, we just add
# # any extra fields that aren't part of the Page model, in this
# # case, date of birth.

class Team(Page):
    pass


class TeamCategory(models.Model):
    order = models.IntegerField()
    category = models.TextField()

    def __unicode__(self):
        return "{self.order}. {self.category}".format(self=self)

    class Meta:
        verbose_name_plural = 'categories'


class TeamComponent(models.Model):
    team = models.ForeignKey("Team")
    img = FileField(("File"), max_length=200, format="Image", upload_to="team")
    name = models.CharField(max_length=40)
    desc = models.TextField()
    category = models.ForeignKey(TeamCategory)

    def __unicode__(self):
        return u"{self.name}".format(self=self)
