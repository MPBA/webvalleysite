from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Team, TeamComponent

class TeamInline(admin.TabularInline):
	model = TeamComponent

class TeamAdmin(PageAdmin):
	inlines = (TeamInline,)

admin.site.register(Team, TeamAdmin)
