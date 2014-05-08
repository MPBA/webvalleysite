import logging
import datetime

from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render as django_render, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test


from website.models import UserProfile

import applicationprocess_settings as app_settings
from forms import ApplicationProcessSelectForm, UploadSignedCopyForm
from models import ApplicationStatus
from applicationprocess_settings import FormStatusChoices, ApplicationStatusChoices
from form_generator import FormFactory
from submissions import do_submission, do_final_submission



logger = logging.getLogger( __name__ )

def render(*args, **kwargs):
    """
    Wraps django.shortcuts.render, adding the proper 'sidebar_item' value
    to the template context
    """
    predef_dict = {'sidebar_item' : 'applicationprocess',
                   'form_status_choices' : FormStatusChoices,
                   'application_status_choices' : ApplicationStatusChoices,
                   }

    if 'dictionary' in kwargs:
        kwargs['dictionary'].update(predef_dict)
    elif len(args) >= 3:
        args[2].update(predef_dict)
    else:
        kwargs['dictionary'] = predef_dict
    return django_render(*args, **kwargs)


def can_edit_application(user):
    profile = UserProfile.objects.get_or_create( user=user )[0]
    if ( not profile.is_webvalley_staff
         and ApplicationStatus.objects.filter(user_profile=profile).exists()
         ):
        a_s = profile.applicationstatus
        today = datetime.date.today()
        if ( (a_s.status == 'S_IPR')  # in progress
             and (a_s.application_process.start <= today)
             and (today <= a_s.application_process.deadline) ):
            return True
    return False

def application_edit_perm_required():
    """
    Place this after django.contrib.auth.decorators.login_required
    """
    # can't use reverse, causes circular dependency
    # TODO: consider an entry in settings?
    return user_passes_test(can_edit_application,
                            login_url=app_settings.APPLICATION_CLOSED_URL)

@login_required
def home(request):
    """
    Checks the application status and renders the template with 
    appropriate parameters
    """
    process_form = None
    user_forms = []

    profile = UserProfile.objects.get_or_create( user=request.user )[0]
    profile_filled = None
    ready_for_submission = None
    can_edit_appl = None

    if profile.is_webvalley_staff:
        status = ApplicationStatusChoices.WEBVALLEY_STAFF
    elif not ApplicationStatus.objects.filter(user_profile=profile).exists():
        status = ApplicationStatusChoices.NOT_SET
        process_form = ApplicationProcessSelectForm()
    else:
        status = ApplicationStatusChoices.ONGOING


        user_forms = sorted(profile.applicationstatus.userform_set.all(), key=lambda u: u.index)
        profile_filled = profile.filled_for_application
        ready_for_submission = profile.applicationstatus.ready_for_submission()
        can_edit_appl = can_edit_application(request.user)

    # print "wei"
    # print user_forms[0].form_data
    # if user_forms[0].form_data:
    #     print True 
    # else: 
    #     print False
    # print user_forms[0].status
    # print 
    return render(request, 'application_process/home.html',
                  {'page_title': 'School Application',
                   'application_status': status,
                   'user_forms': user_forms,
                   'choose_process_form': process_form,
                   'profile_filled': profile_filled,
                   'ready_for_submission': ready_for_submission,
                   'can_edit_application': can_edit_appl,
                   })


@require_POST
@transaction.atomic
@login_required()
def set_application_process(request):
    form = ApplicationProcessSelectForm(request.POST)
    if form.is_valid():
        form.save(request.user)
        return HttpResponseRedirect(
            reverse('applicationprocess.views.home'))
    else:
        return render(request,
                      'application_process/home.html',
                      {'page_title': 'School Application',
                       'application_status': ApplicationStatusChoices.NOT_SET,
                       'choose_process_form': form})


@transaction.atomic
@login_required
@application_edit_perm_required()
def form_edit(request, form_id):
    user_form = request.user.get_profile() \
        .applicationstatus.userform_set.get( form__pk=form_id )
    FormClass = FormFactory.form_from_user_form( user_form )
    form_name = user_form.form.name

    if request.method == "POST":
        form = FormClass( request.POST )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('applicationprocess.views.home'))
    elif (user_form.form_data and user_form.form_data <> '{}'):
        form = FormClass( initial=user_form.form_data )
    else:
        form = FormClass(initial = {})
    # else:
    #     form = FormClass( initial=user_form.form_data if user_form.form_data else {} )

    template = user_form.form.template
    if not template:
        template = 'application_process/form_edit.html'

    return render(request,
                  'application_process/form_edit.html',
                  {
                    'form_name':form_name,
                    'form':form
                  })

@transaction.atomic
@login_required
@application_edit_perm_required()
def submit_signed(request, form_id):
    user_form = request.user.get_profile()\
        .applicationstatus.userform_set.get( form__pk=form_id )
    form_name = user_form.form.name

    if request.method == "POST":
        form = UploadSignedCopyForm( request.POST, request.FILES, instance=user_form )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('applicationprocess.views.home'))
    else:
        form = UploadSignedCopyForm(instance=user_form)

    return render(request,
                  'application_process/form_upload.html',
                  {
                    'form_name':form_name,
                    'form':form
                  })

@transaction.atomic
@login_required
@application_edit_perm_required()
def submit(request):
    if request.method == 'GET':
        return render(request, 'application_process/submit_confirm.html')
    elif request.method == 'POST':
        profile = request.user.get_profile()
        if profile.applicationstatus.ready_for_submission():
            do_submission( profile )
            do_final_submission( profile )
            a_s = profile.applicationstatus
            a_s.staftus = 'S_SUB'
            a_s.save()
            return render(request, 'application_process/submit_done.html')
        else:
            return render(request, 'application_process/submit_confirm.html')
        
@login_required
def closed(request):
    return render(request, 'application_process/closed.html')
