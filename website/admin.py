from django.contrib import admin
from .models import UserProfile, Country


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', '__unicode__', 'nationality', 'gender', 'birth_date', 'key_expires', 'get_user')
    list_filter = ('key_expires', 'nationality', 'gender', 'user__is_active')
    search_fields = ('user__first_name', 'nationality__name')

    def get_user(self, obj):
        return obj.user.is_active

    get_user.short_description = 'Active'


admin.site.register(Country)
# admin.site.register(WebValleyEdition)
admin.site.register(UserProfile, ProfileAdmin)
# admin.site.register(Document)
# admin.site.register(DocumentType)
