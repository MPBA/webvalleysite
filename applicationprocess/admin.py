from django.contrib import admin
from django.core.exceptions import PermissionDenied
from models import Form, ApplicationProcess, Validator, \
    Field, FieldType, ValidatorType, ApplicationStatus, ApplicationProcessForm, UserForm, APPLICATION_STATUS_OPTIONS
from website.models import UserProfile
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
    actions = [export_as_csv, 'set_application_status_as_old', 'download_complete_csv']

    def changelist_view(self, request, extra_context=None):
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            action_acts_on_all = action.acts_on_all
        except (KeyError, AttributeError):
            action_acts_on_all = False

        if action_acts_on_all:
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME,
                        self.model.objects.values_list('id', flat=True))
            request.POST = post

        return admin.ModelAdmin.changelist_view(self, request, extra_context)

    def set_application_status_as_old(self, request, queryset):
        rows_updated = queryset.update(status='S_OLD')
        if rows_updated == 1:
            message_bit = "1 application was"
        else:
            message_bit = "%s applications were" % rows_updated
        self.message_user(request, "%s successfully marked as old." % message_bit)

    def download_complete_csv(self, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/ and /2020/
        """
        if not request.user.is_staff:
            raise PermissionDenied
        opts = self.model._meta

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        
        email = ""
        first_name = ""
        last_name = ""
        nationality = ""
        gender = ""
        birth_date = ""
        birth_place = ""
        home_phone = ""
        mobile_phone = ""
        city = ""
        street1 = ""
        street2 = ""
        country = ""
        state = ""
        postalCode = ""
        school = ""
        schoolAddress = ""
        referenceProfessor = ""

        writer.writerow([
            "email",
            "first name",
            "last name",
            "nationality",
            "gender",
            "birth_date",
            "birth_place",
            "home phone",
            "mobile_phone",
            "city",
            "street 1",
            "street 2",
            "country",
            "state",
            "postal code",
            "school",
            "school address",
            "reference professor"
        ])

        submitted_appications = ApplicationStatus.objects.filter(status="S_SUB")
        
        for row in submitted_appications:
            values = []
            user_forms = UserForm.objects.filter(application_status=row.id)
            
            for user_form in user_forms:
                if str(user_form.form) == "Home Address":
                    city = (user_form.form_data["City"].encode('utf-8'))
                    street1 = (user_form.form_data["Street 1"].encode('utf-8'))
                    street2 = (user_form.form_data["Street 2"].encode('utf-8'))
                    country = (user_form.form_data["Country"].encode('utf-8'))
                    state = (user_form.form_data["State Province"].encode('utf-8'))
                    postalCode = (user_form.form_data["Postal code"].encode('utf-8'))
                if str(user_form.form) == "School":
                    school = (user_form.form_data["Name of the School"].encode('utf-8'))
                    schoolAddress = (user_form.form_data["School's Address"].encode('utf-8'))
                    referenceProfessor = (user_form.form_data["Reference Professor"].encode('utf-8'))
                
            email = getattr(row, "email")()
            user_profile = UserProfile.objects.filter(applicationstatus=row.id)
            first_name = user_profile[0].first_name
            last_name = user_profile[0].last_name
            nationality = user_profile[0].nationality
            gender = user_profile[0].gender
            birth_date = user_profile[0].birth_date
            birth_place = user_profile[0].birth_place
            home_phone = user_profile[0].home_phone
            mobile_phone = user_profile[0].mobile_phone

            values.append(email)
            values.append(first_name)
            values.append(last_name)
            values.append(nationality)
            values.append(gender)
            values.append(birth_date)
            values.append(birth_place)
            values.append(home_phone)
            values.append(mobile_phone)
            values.append(city)
            values.append(street1)
            values.append(street2)
            values.append(country)
            values.append(state)
            values.append(postalCode)
            values.append(school)
            values.append(schoolAddress)
            values.append(referenceProfessor)

            writer.writerow(values)
        return response

    set_application_status_as_old.short_description = "Mark selected application as old"
    download_complete_csv.short_description = "Download all submitted applications"
    download_complete_csv.acts_on_all = True
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
