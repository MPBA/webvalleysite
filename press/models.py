from django.db import models
from mezzanine.pages.models import Page
# # The members of Page will be inherited by the Author model, such
# # as title, slug, etc. For authors we can use the title field to
# # store the author's name. For our model definition, we just add
# # any extra fields that aren't part of the Page model, in this
# # case, date of birth.

class Press(Page):
	pass

class PressEvent(models.Model):
    press = models.ForeignKey("Press")
    date = models.DateField(max_length=40)
    title = models.TextField()
    link =  models.TextField()
