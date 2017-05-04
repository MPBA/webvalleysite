from django.contrib import admin
from .models import AlumniStudent

# Register your models here.
class AlumniInline(admin.TabularInline):
    model = AlumniStudent

class AlumniComponentAdmin(admin.ModelAdmin):
    list_display = ('name','desc')

admin.site.register(AlumniStudent, AlumniComponentAdmin)
