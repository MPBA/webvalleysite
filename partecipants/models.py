from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import FileField
# # The members of Page will be inherited by the Author model, such
# # as title, slug, etc. For authors we can use the title field to
# # store the author's name. For our model definition, we just add
# # any extra fields that aren't part of the Page model, in this
# # case, date of birth.

class Partecipants(Page):
	pass

class Person(models.Model):
	partecipants = models.ForeignKey(Partecipants)
	photo = FileField(("File"), max_length=200, format="Image", upload_to="partecipants")
	name = models.CharField(max_length=40)
	city = models.CharField(max_length=80)
	confirmed = models.BooleanField()
