from __future__ import print_function
from alumni.models import AlumniStudent
from django.shortcuts import render
from alumni.forms import AlumniStudentForm
from django.conf import settings

def alumni_views(request):
    alumnis = AlumniStudent.objects.filter(approved=True)
    context = {}
    context['alumnis'] = alumnis
    if request.method == "GET":
        context['form'] = AlumniStudentForm()
    elif request.method == "POST":
        form = AlumniStudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context['form'] = AlumniStudentForm()
            context['success'] = "Thank you! An administrator will approve your alumni submission as soon as possible."
        else:
            context['form'] = form
    context['api_key'] = settings.GOOGLE_APIS_KEY
    return render(request, "alumni/alumni.html", context)
