from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import Timetable

# timetable_login_fields = ((None, {"fields": ("google_user", "google_passwd", "spreadsheet", "spreadsheet_gid")}),)

class TimetableAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) # + timetable_login_fields

admin.site.register(Timetable, TimetableAdmin)
