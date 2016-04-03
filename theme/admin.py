from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("date_joined", 'is_active')
    actions = UserAdmin.actions + ['deactivate_users']

    def deactivate_users(self, request, queryset):
        # remove staff or super users from the selected ones
        queryset = queryset.filter(is_superuser=False, is_staff=False)

        rows_updated = queryset.update(is_active=False)
        if rows_updated == 1:
            message_bit = "1 user was"
        else:
            message_bit = "%s users were" % rows_updated
        self.message_user(request, "%s successfully deactivated." % message_bit)

    deactivate_users.short_description = "Deactivate selected users"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
