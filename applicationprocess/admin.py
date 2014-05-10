from django.contrib import admin
from models import Form,ApplicationProcess,Validator,\
    Field, FieldType, ValidatorType, ApplicationStatus, ApplicationProcessForm, UserForm
from django.http import HttpResponse
import csv


def extract_email(modeladmin, request, queryset):
	for obj in queryset:
		print obj.email()

extract_email.short_description = "Extract email"

# def export_as_csv(description="Download selected rows as CSV file",header=True):
#     """
#     This function returns an export csv action
#     This function ONLY downloads the columns shown in the list_display of the admin
#     'header' is whether or not to output the column names as the first row
#     """
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

#     export_as_csv.short_description = description
#     return export_as_csv

class ApplicationStatusAdmin(admin.ModelAdmin):
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name')
    list_filter = ('application_process', 'status')
    list_display = ('__unicode__', 'email',)
    actions = [export_as_csv]

class UserFormAdmin(admin.ModelAdmin):
    search_fields = ('application_status__user_profile__user__first_name', 'application_status__user_profile__user__last_name')
    list_filter = ('form',)

admin.site.register(Form)
admin.site.register(ApplicationProcess)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(Validator)
admin.site.register(ValidatorType)
admin.site.register(Field)
admin.site.register(FieldType)
admin.site.register(ApplicationProcessForm)
admin.site.register(UserForm, UserFormAdmin)



# from mezzanine.utils.models import get_user_model
# from mezzanine.core.admin import SitePermissionUserAdmin

# class UserAdmin(SitePermissionUserAdmin):
# 	list_display = SitePermissionUserAdmin.list_display + ('date_joined',)
# 	list_filter = SitePermissionUserAdmin.list_filter + ('date_joined',)
# 	search_fields = ('date_joined',)

# User = get_user_model()
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)