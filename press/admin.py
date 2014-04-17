from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Press, PressEvent

class PressInLine(admin.TabularInline):
	model = PressEvent

class PressAdmin(PageAdmin):
	inlines = (PressInLine,)

admin.site.register(Press, PressAdmin)
