from django.contrib import admin
from django.core.exceptions import PermissionDenied
from models import Form, ApplicationProcess, Validator, \
    Field, FieldType, ValidatorType, ApplicationStatus, ApplicationProcessForm, UserForm, APPLICATION_STATUS_OPTIONS
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
    list_display = ('__unicode__', 'email', 'status')
    actions = [export_as_csv, 'set_application_status_as_old']

    def set_application_status_as_old(self, request, queryset):
        rows_updated = queryset.update(status='S_OLD')
        if rows_updated == 1:
            message_bit = "1 application was"
        else:
            message_bit = "%s applications were" % rows_updated
        self.message_user(request, "%s successfully marked as old." % message_bit)

    set_application_status_as_old.short_description = "Mark selected application as old"

    ordering = ('status',)


class UserFormAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'get_status',)
    search_fields = (
        'application_status__user_profile__user__first_name', 'application_status__user_profile__user__last_name')
    list_filter = ('form', 'application_status__status')

    def get_status(self, obj):
        return obj.application_status.get_status_display()

    get_status.short_description = 'Application Status'

    ordering = ('application_status__status',)


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
