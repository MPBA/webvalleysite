from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import FileField
from django.core.validators import MaxValueValidator, MinValueValidator

# # The members of Page will be inherited by the Author model, such
# # as title, slug, etc. For authors we can use the title field to
# # store the author's name. For our model definition, we just add
# # any extra fields that aren't part of the Page model, in this
# # case, date of birth.

class AlumniStudent(models.Model):
    img = FileField(("File"), max_length=200, format="Image", upload_to="alumni")
    name = models.CharField(max_length=40)
    desc = models.TextField()
    year_in_school = models.IntegerField(
        choices=((year, str(year)) for year in range(2001, 2018)),
    )
    loc_string = models.CharField(max_length=100)
    lat = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    lon = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])

    def __unicode__(self):
        return u"{self.name}".format(self=self)
