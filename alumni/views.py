from alumni.models import AlumniStudent
from django.shortcuts import render
from alumni.forms import AlumniStudentForm

def alumni_views(request):
    alumnis = AlumniStudent.objects.all()
    context = {}
    context['alumnis'] = alumnis
    context['form'] = AlumniStudentForm()
    return render(request, "alumni/alumni.html", context)
