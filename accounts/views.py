import hashlib
import random
import time
import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.utils.timezone import utc

from theme.views import home
from website.models import UserProfile
from applicationprocess.models import ApplicationStatus

from .forms import RegistrationForm
from .accounts_settings import CONFIRMATION_EMAIL_SUBJECT, CONFIRMATION_EMAIL_TEMPLATE, WEBVALLEY_EMAIL_ADDRESS
from local_settings import DEBUG

def signup(request):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return home(request, errors=[_('You already have an account!')])

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            with transaction.atomic():
                new_user = create_new_inactive_user(first_name=form.cleaned_data['first_name'],
                                                    last_name=form.cleaned_data['last_name'],
                                                    email=form.cleaned_data['mail'],
                                                    password=form.cleaned_data['password1'])
                new_user.save()

                new_profile = create_new_profile( new_user )
                new_profile.save()



                if not DEBUG:
                    send_confirmation_email( new_user )

            return home(request, notifications=[_('Your account has been created. Check your email and follow the instructions to activate it.')])
    else:
        form = RegistrationForm()

    form = str(form).replace('<tr><th>', '<div class="form-group">').replace('</th><td>', '').replace('</td></tr>', '</div>')
    return render(request, 'signup.html', {'form': form, 'sidebar_item': 'signup', 'page_title': 'signup'})


def confirm(request, activation_key):
    if request.user.is_authenticated():
        return home(request, errors = [_('You already have an account')])
    if not DEBUG:
        user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except UserProfile.DoesNotExist:
        return home(request, errors = [_(u'Your activation key is not valid. It likely expired. If you have a working account, please log in with your email and password; if you don\'t, simply sign up.')])

    user_account = user_profile.user
    if user_profile.user.is_active:
        return HttpResponseRedirect('/')
    elif user_profile.key_expires < datetime.datetime.utcnow().replace(tzinfo=utc):
        user_account.delete()
        return home(request, errors = [_('Your activation key has expired.')])
    else: # everythig is right
        user_account.is_active = True
        user_account.save()
        return home(request, notifications=[_('Your account has been activated')])

def login(request):
    next_page = request.GET.get('next', '/')
    if request.method == 'POST' and ( request.POST.get('username', '') or request.POST.get('password', '')):
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

        # try to authenticate the user
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            if user.is_active:
                auth_views.login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                return home(request, errors=[_("Account is disabled.")])
        else:
            # invalid login
            return home(request, errors=[_("Invalid username or password.")])
    else:
        return render(request, 'login.html', {'next_page': next_page,
                                                      'sidebar_item':'login',
                                                      'page_title': 'account/login',
												'application_status': ApplicationStatus.status})

def logout(request):
    next_page = "/"

    if request.GET and request.GET['next']:
        next_page = request.GET['next']

    return auth_views.logout(request, next_page=next_page)


def send_confirmation_email( new_user ):
    context = { 'confirmation_key' : new_user.get_profile().activation_key,
                'first_name' : new_user.first_name,
                'website_url' : Site.objects.get_current().domain}
    mail_body = render_to_string( CONFIRMATION_EMAIL_TEMPLATE, context )
    send_mail( CONFIRMATION_EMAIL_SUBJECT, mail_body, WEBVALLEY_EMAIL_ADDRESS, [new_user.email], fail_silently=False)

def make_username(first_name, last_name):
    # first three characters of the name, first three characters of the surname and the unix timestamp.
    return first_name[:3] + last_name[:3] + str(time.time()).replace('.','')

def create_new_inactive_user( first_name, last_name, email, password ):
    new_user = User.objects.create_user( make_username(first_name, last_name), password=password, email=email)
    new_user.is_active = False
    new_user.first_name = first_name
    new_user.last_name = last_name
    return new_user

def create_new_profile( new_user ):
    # Build the activation key for the
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + new_user.username.encode('utf-8')).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    new_profile = UserProfile( user=new_user, activation_key=activation_key, key_expires=key_expires )
    return new_profile
