from django.contrib import admin
from .models import UserProfile, Country


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', '__unicode__', 'nationality', 'gender', 'birth_date', 'key_expires',)
    list_filter = ('key_expires', 'nationality', 'gender')
    search_fields = ('user__first_name', )


admin.site.register(Country)
#admin.site.register(WebValleyEdition)
admin.site.register(UserProfile, ProfileAdmin)
#admin.site.register(Document)
#admin.site.register(DocumentType)



