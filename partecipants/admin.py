from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Partecipants, Person

class PersonInLine(admin.TabularInline):
	model = Person

class PartecipantsAdmin(PageAdmin):
	inlines = (PersonInLine,)

admin.site.register(Partecipants, PartecipantsAdmin)
