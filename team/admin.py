from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Team, TeamComponent, TeamCategory


class TeamInline(admin.TabularInline):
    model = TeamComponent


class TeamAdmin(PageAdmin):
    inlines = (TeamInline,)


class TeamComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'category')


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamComponent, TeamComponentAdmin)
admin.site.register(TeamCategory)
