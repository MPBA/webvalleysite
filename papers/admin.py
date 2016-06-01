from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import PaperPage, Paper


class PaperInLine(admin.TabularInline):
    model = Paper


class PaperPageAdmin(PageAdmin):
    inlines = (PaperInLine,)


admin.site.register(PaperPage, PaperPageAdmin)
