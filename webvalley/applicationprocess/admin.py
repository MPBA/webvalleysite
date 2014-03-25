from django.contrib import admin
from models import Form,ApplicationProcess,Validator,\
    Field,FieldType,ValidatorType,ApplicationStatus,ApplicationProcessForm,UserForm

class ApplicationStatusAdmin(admin.ModelAdmin):
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name')
    list_filter = ('application_process', 'status')

admin.site.register(Form)
admin.site.register(ApplicationProcess)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(Validator)
admin.site.register(ValidatorType)
admin.site.register(Field)
admin.site.register(FieldType)
admin.site.register(ApplicationProcessForm)
admin.site.register(UserForm)
