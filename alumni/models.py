from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class AlumniStudent(models.Model):
    img = models.ImageField(upload_to="alumni", default='/static/misc/generic-alumni.png')
    name = models.CharField(max_length=40)
    desc = models.TextField(blank=True, default='')
    year_in_school = models.IntegerField(
        choices=((year, str(year)) for year in range(2001, 2018)),
    )
    email = models.EmailField()
    loc_string = models.CharField(max_length=100)
    birth_place = models.CharField(max_length=100, null=True, blank=True)
    lat = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    lon = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{self.name}".format(self=self)
