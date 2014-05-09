from django.contrib import admin
from models import Form,ApplicationProcess,Validator,\
    Field, FieldType, ValidatorType, ApplicationStatus, ApplicationProcessForm, UserForm

class ApplicationStatusAdmin(admin.ModelAdmin):
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name')
    list_filter = ('application_process', 'status')
    list_display = ('__unicode__', 'email',)

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