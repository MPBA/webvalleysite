from __future__ import unicode_literals

from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required

from forms import EditProfileForm, UploadPaperForm, CreateDirForm

from website.models import UserProfile
from django.template import RequestContext
from local_settings import DEBUG
import sys
from django.conf import settings

import zipfile
import os, stat
from cStringIO import StringIO

from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def my(request):
    return render(request, 'profile/my.html', {
        'page_title': 'profile/view',
        'sidebar_item': 'view-profile',
    })


@login_required
def edit(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/my/')
        else:
            form = EditProfileForm(request.POST, request.FILES, instance=profile)
            return render(request, 'profile/edit.html', {'form': form})

    else:
        profile.birth_date = profile.birth_date.strftime("%m/%d/%Y") if profile.birth_date else profile.birth_date
        form = EditProfileForm(instance=profile)
        return render(request, 'profile/edit.html',
                      {'form': form,
                       'page_title': 'profile/edit',
                       'sidebar_item': 'view-profile'})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_zip(request, dir, name):
    dir = os.path.join(settings.PROJECT_ROOT, dir)
    relroot = os.path.abspath(os.path.join(dir, os.pardir))
    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'filename=%s.zip' % name
    zipfile_final = StringIO()
    with zipfile.ZipFile(zipfile_final, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(dir):
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename):
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                zip.write(filename, arcname)
        zip.close()
    zipfile_final.seek(0)
    response.write(zipfile_final.read())
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def browse_applications(request, url):
    def_path = os.getcwd()
    path = settings.PROJECT_ROOT
    myfiles = os.path.join(path, 'static/media/')
    mylist = os.path.join(myfiles, url)
    os.chdir(mylist)
    files = os.listdir(".")
    file_dict = []

    for f in files:
        print f
        if os.path.isdir(f):
            file_dict.append({'name': f, 'link': os.path.join(url, f), 'download': os.path.join('static/media', url, f),
                              'type': 'directory'})
        else:
            file_dict.append({'name': f, 'link': os.path.join('/static/media', url, f), 'type': 'file'})
    context = {'filelist': file_dict}
    os.chdir(def_path)
    return render_to_response('profile/read_apps.html', context, context_instance=RequestContext(request))


@login_required
def browse_paper(request, url):
    def_path = os.getcwd()
    path = settings.PROJECT_ROOT
    myfiles = os.path.join(path, 'static/media/uploads/papers/')
    mylist = os.path.join(myfiles, url)
    os.chdir(mylist)
    if request.method == 'POST':
        form = UploadPaperForm(request.POST, request.FILES['file'])
        # if form.is_valid():
        handle_uploaded_file(request.FILES.getlist('file'), dir='.')

    files = os.listdir(".")
    file_dict = []
    print url
    for f in files:
        print url
        if os.path.isdir(f):
            file_dict.append({'name': f, 'link': os.path.join(url, f),
                              'download': os.path.join('static/media/uploads/papers', url, f), 'type': 'directory'})
        else:
            file_dict.append({'name': f, 'link': os.path.join('/static/media/uploads/papers', url, f),
                              'download': os.path.join('static/media/uploads/papers', url), 'type': 'file'})
    context = {'filelist': file_dict,
               'form': UploadPaperForm(),
               'formdir': CreateDirForm(),
               'myurl': url}
    os.chdir(def_path)
    return render_to_response('profile/read_papers.html', context, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_file(request, myurl, mydir):
    path = settings.PROJECT_ROOT
    myfile = os.path.join(path, myurl, mydir)
    os.remove(myfile)
    return redirect(browse_paper, url="")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def make_dir(request, url):
    if request.method == 'POST':
        form = CreateDirForm(request.POST)
        path = settings.PROJECT_ROOT
        myfiles = os.path.join(path, 'static/media/uploads/papers/')
        mylist = os.path.join(myfiles, url)
        os.chdir(mylist)
        os.mkdir(request.POST['mydir'])
    return redirect('browse_papers', url="")


def test_view(request):
    return render(request, 'profile/read_apps.html',
                  {
                      'page_title': 'profile/test',
                      'sidebar_item': 'view-profile'})


def handle_uploaded_file(f, dir):
    for ff in f:
        with open('{}'.format(ff.name), 'wb+') as destination:
            for chunk in ff.chunks():
                destination.write(chunk)
