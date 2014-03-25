from django.db import models
from mezzanine.pages.models import Page

class Timetable(Page):
	google_user = models.CharField( "Google User", max_length=20)
	google_passwd = models.CharField("Google password", max_length=20)
	spreadsheet = models.CharField( "Spreadsheet", max_length=50)
	spreadsheet_gid = models.IntegerField("GID")

# class Author(Page):
#     dob = models.DateField("Date of birth")

# class Book(models.Model):
#     author = models.ForeignKey("Author")
#     cover = models.ImageField(upload_to="authors")
