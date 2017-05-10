from __future__ import print_function
from alumni.models import AlumniStudent
from django.shortcuts import render
from alumni.forms import AlumniStudentForm, AlumniApprovalForm
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse, HttpResponseBadRequest

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

@staff_member_required
def alumni_approval_view(request):
    alumnis = AlumniStudent.objects.all()
    context = {}
    if request.method == "GET":
        context['alumnis'] = alumnis
        context['form'] = AlumniApprovalForm()
    elif request.method == "POST":
        form = AlumniApprovalForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            a = AlumniStudent.objects.get(id=payload['id'])
            a.approved = payload['approved']
            a.save()
            return HttpResponse("{}".format(a.approved))
        else:
            return HttpResponseBadRequest()
    return render(request, "alumni/alumni_approval.html", context)
