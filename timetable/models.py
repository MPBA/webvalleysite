from django.db import models
from mezzanine.pages.models import Page
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField
from django.contrib.auth.models import User
from django.db import models
from oauth2client.django_orm import CredentialsField


class Timetable(Page):
    google_user = models.CharField("Google User", max_length=20)
    google_passwd = models.CharField("Google password", max_length=20)
    spreadsheet = models.CharField("Spreadsheet", max_length=50)
    spreadsheet_gid = models.IntegerField("GID")

