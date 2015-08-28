from django.contrib import admin
from django.core.exceptions import PermissionDenied
from models import Form,ApplicationProcess,Validator,\
    Field, FieldType, ValidatorType, ApplicationStatus, ApplicationProcessForm, UserForm
from django.http import HttpResponse
import csv

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    based on http://djangosnippets.org/snippets/1697/ and /2020/
    """
    # TODO Also create export_as_csv for exporting all columns including list_display
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    field_names = modeladmin.list_display
    if 'action_checkbox' in field_names:
        field_names.remove('action_checkbox')

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

    writer = csv.writer(response)
    for row in queryset:
        values = []
        for field in field_names:
            value = (getattr(row, field))
            if callable(value):
                try:
                    value = value() or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(unicode(value).encode('utf-8'))
        writer.writerow(values)
    return response

class ApplicationStatusAdmin(admin.ModelAdmin):
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name')
    list_filter = ('application_process', 'status')
    list_display = ('__unicode__', 'email',)
    actions = [export_as_csv]

class UserFormAdmin(admin.ModelAdmin):
    search_fields = ('application_status__user_profile__user__first_name', 'application_status__user_profile__user__last_name')
    list_filter = ('form',)


class ApplicationProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'deadline',)


admin.site.register(Form)
admin.site.register(ApplicationProcess, ApplicationProcessAdmin)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(Validator)
admin.site.register(ValidatorType)
admin.site.register(Field)
admin.site.register(FieldType)
admin.site.register(ApplicationProcessForm)
admin.site.register(UserForm, UserFormAdmin)
