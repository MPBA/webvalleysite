from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

from forms import EditProfileForm

from website.models import UserProfile
from django.template import RequestContext
from local_settings import DEBUG
import sys
from django.conf import settings

import zipfile
import os,stat
from cStringIO import StringIO

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def my(request):
    return render(request, 'profile/my.html', {
        'page_title' : 'profile/view',
        'sidebar_item' : 'view-profile',
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
    path = settings.PROJECT_ROOT
    myfiles = os.path.join(path, 'static/media/')
    mylist = os.path.join(myfiles, url)
    #os.chdir(mylist)
    files = os.listdir(mylist)
    file_dict = []

    for f in files:
        if os.path.isdir(f):
            file_dict.append({'name': f, 'link': os.path.join(url, f), 'download':  os.path.join('static/media', url, f), 'type': 'directory'})
        else:
            file_dict.append({'name': f, 'link': os.path.join('/static/media', url, f), 'type': 'file'})
    context = {'filelist': file_dict}
    return render_to_response('profile/read_apps.html', context, context_instance=RequestContext(request))


def test_view(request):
    return render(request, 'profile/read_apps.html',
                {
                 'page_title': 'profile/test',
                 'sidebar_item': 'view-profile'})
