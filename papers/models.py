from django.db import models
from mezzanine.pages.models import Page
import datetime
import os


# # The members of Page will be inherited by the Author model, such
# # as title, slug, etc. For authors we can use the title field to
# # store the author's name. For our model definition, we just add
# # any extra fields that aren't part of the Page model, in this
# # case, date of birth.

class PaperPage(Page):
    _get_current_year = lambda: datetime.date.today().year

    year = models.IntegerField(default=_get_current_year)


class Paper(models.Model):
    paperpage = models.ForeignKey("PaperPage")
    year = models.IntegerField()
    authors = models.TextField()
    title = models.TextField()

    _get_upload_to = (lambda instance, filename: os.path.join(
        "uploads",
        "papers",
        filename))
    paper = models.FileField(upload_to=_get_upload_to, blank=False, null=False)

    class Meta:
        ordering = ['year']