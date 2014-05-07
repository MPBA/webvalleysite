from __future__ import print_function
from sys import argv
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileMerger
import shutil
import os
import json
import csv
import codecs
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ordereddict import OrderedDict

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from django.conf import settings

from applicationprocess_settings import APPLICATIONPROCESS_EMAIL_SUBJECT,\
    APPLICATIONPROCESS_HANDLER_EMAILS,USER_DATA_ROOT
from accounts.accounts_settings import WEBVALLEY_EMAIL_ADDRESS


def do_submission( user_profile ):
    """
    Makes a copy of the user data into a specific folder.
    Send a confirmation email both to the handler and to the user
    """

    user_number = user_profile.applicationstatus.pk
    application_process_name = user_profile.applicationstatus.application_process.name
    data_path = os.path.join(USER_DATA_ROOT,application_process_name,str(user_number))

    if os.path.exists( data_path ):
        # if data_path exists, rename it appending _old_num where num is a counter
        n = 1
        while( True ):
            new_path = os.path.join(data_path, '..', str(user_number) + '_old_' + str(n))
            if not os.path.exists( new_path ):
                break
            n += 1
        shutil.move( data_path, new_path )
            
            

    shutil.copytree(
        os.path.join(
            settings.MEDIA_ROOT,
            'docs',
            user_profile.user.username),
        data_path
    )

    with open( os.path.join( data_path, 'data.json'), 'w' ) as data_file:
        data_file.write( _get_json( _get_data( user_profile ) ) )

    with codecs.open( os.path.join(data_path, 'data.csv'), 'w', encoding='utf-8' ) as data_file:
        data_file.write( _get_csv( _get_csv_data( user_profile ) ) )

def do_final_submission( user_profile ):
    """
    Places a copy of the user's data into a folder containing only submitted applications
    """
    user_number = user_profile.applicationstatus.pk
    user_name = " ".join( [str(user_profile.user.last_name), str(user_profile.user.first_name)] )
    application_process_name = user_profile.applicationstatus.application_process.name
    data_path = os.path.join(USER_DATA_ROOT, "submitted_applications", application_process_name, user_name)

    if os.path.exists( data_path ):
        # if data_path exists, so there are namesakes, rename it appending _num where num is a counter
        n = 1
        while( True ):
            new_path = os.path.join(data_path, '..', str(user_number) + str(n))
            if not os.path.exists( new_path ):
                break
            n += 1
        shutil.move( data_path, new_path )

    shutil.copytree(
        os.path.join(
            settings.MEDIA_ROOT,
            'docs',
            user_profile.user.username),
        data_path
    )

    """
	generate json
    """
    with open( os.path.join( data_path, 'data.json'), 'w' ) as data_file:
        data_file.write( _get_json( _get_data( user_profile ) ) )

    """
	generate csv
    """
    with codecs.open( os.path.join( data_path, 'data.csv'), 'w', encoding='utf-8' ) as data_file:
        data_file.write( _get_csv( _get_csv_data( user_profile ) ) )

    """
	generate pdf (without the 'School report, CV and certifications' and the form accepted part)
    """
    with open (os.path.join(data_path, 'data.json'), 'r') as json_file:
        js = json.load(json_file)

    js.pop('School report, CV and certifications')
    js.pop("Code of Conduct") 
    js.pop("Parent Agreement") 
    js.pop("Assignment of Laptop") 
    js.pop("Media Consent Form")
    js.pop("Motivation letter") 

    with open( os.path.join( data_path, 'tmp.json'), 'w' ) as data_file:
        data_file.write(_get_json(js))

    with open (os.path.join(data_path, 'tmp.json'), 'r') as json_file:
        data=json_file.read()
    os.remove(os.path.join( data_path, 'tmp.json'))

    data = data.replace("{", "")
    data = data.replace("}", "")
    data = data.replace("\"", "")
    data = data.replace(",", "")
    filename = "".join([str(user_name),".pdf"])
    profile_picture = os.listdir(data_path) # submitted folder
    for file in profile_picture:
        if file.startswith('profile'):
            profile_picture = file
            break;

    point = 1
    inch = 72
    pagesize = (8.5 * inch, 11 * inch)
    c = canvas.Canvas('tmp', pagesize=pagesize)
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    line_height = point * 11
    c.setFont("Courier", line_height)
    v = line_height
    for subtline in data.split( '\n' ):
        c.drawString( 1 * inch, v, subtline )
        v -= line_height * 2 # Jump a line

    c.drawImage('profile.jpg', pagesize[0] - 200, pagesize[1] - 200, 150, 150, preserveAspectRatio=True)
    c.save()

    """
    merge pdf in signed-form
    """
    merger = PdfFileMerger()
    merger.strict = False
    sf_dir = os.path.join(data_path, 'signed-forms')
    for filename in os.listdir(sf_dir):
        if os.path.splitext(filename)[1].lower() == '.pdf':
            merger.append(PdfFileReader(open(os.path.join(sf_dir, filename), 'rb'), strict=False))

    merger.write(open(os.path.join(data_path, 'signed-forms', 'merged_pdf.pdf'), 'wb'))

    _send_submission_email_to_user( user_profile )
    _send_submission_email_to_handler( user_profile, data_path, user_number )


def _get_json( data ):
    return json.dumps( data, indent=4 ) #.decode('utf-8') # non funziona...

def _get_data( user_profile ):
    data = OrderedDict()
    data [ 'profile' ] = _get_profile_data( user_profile ) 
    data.update( _get_form_data( user_profile ))
    return data

def _get_profile_data( user_profile ):
    data = OrderedDict()

    more_fields = ['first_name', 'last_name', 'email', 'username']

    for field in more_fields + user_profile._application_needed_fields :
        field_data = getattr( user_profile, field, "ERROR" )
        if field == 'nationality':
            field_data = field_data.name
        elif field == 'birth_date':
            field_data = str(field_data)
        elif field == 'photo':
            field_data = 'http://' + Site.objects.get_current().domain + field_data.url

        data[field] = field_data

    return data

def _get_form_data( user_profile ):
    data = OrderedDict()
    #for user_form in user_profile.applicationstatus.userform_set.all():
    for user_form in sorted( user_profile.applicationstatus.userform_set.all(),
                             key=lambda u: u.index ):
        data[ user_form.form.name ] = user_form.form_data
    return data

def _get_csv( data ):
    buf = StringIO()
    out = csv.writer( buf )
    out.writerow( [(u.encode('utf-8') if type(u)==unicode else u) for u in _header_flatten( data )] )
    out.writerow( [(u.encode('utf-8') if type(u)==unicode else u) for u in _data_flatten( data )] )
    return buf.getvalue().decode('utf-8')
    #return repr(_header_flatten( data )) + u'\n' + repr(_data_flatten( data ))

def _data_flatten( data ):
    if isinstance( data, dict ):
        l = []
        for val in data.values():
            l.extend(_data_flatten(val))
        return l
    else:
        return [ data ]

def _header_flatten( data, prefix=u'' ):
    if isinstance( data, dict ):
        l = []
        for key,val in data.items():
            newprefix = u'>'.join( (prefix, key) ) if prefix else key
            l.extend( _header_flatten( val, newprefix ) )
        return l
    else:
        return [ prefix ]

#def _header_flatten( data ):
#    if isinstance( data, OrderedDict ):
#        return [ _header_flatten( val ) for val in data.keys() ]
#    else:
#        return [ data ]

def _get_csv_data( user_profile ):
    data = OrderedDict()
    data [ 'application_status_ID' ] = user_profile.applicationstatus.pk
    data [ 'profile' ] = _get_profile_data( user_profile ) 
    data.update( _get_csv_form_data( user_profile ))
    #data ['optional_subjects'] = _get_other_subjects_data( user_profile )
    return data

def _get_csv_form_data( user_profile ):
    data = OrderedDict()
    #for user_form in user_profile.applicationstatus.userform_set.all():
    for user_form in sorted( user_profile.applicationstatus.userform_set.all(),
                             key=lambda u: u.index ):
        if u'School report, CV and certifications' in user_form.form.name:
            data[ user_form.form.name ] = OrderedDict()
            for field in user_form.form.fields.all(): # TODO: filter dictfields...
                data[ user_form.form.name ][ field.name ] = OrderedDict()
                for subject in field.extra_options[u'mandatory_choices']:
                    data[ user_form.form.name ][ field.name ][ subject ] = \
                        user_form.form_data[ field.name ][ subject ]
        else:
            data[ user_form.form.name ] = user_form.form_data
            
    return data

def _get_other_subjects_data( user_profile ):
    data = OrderedDict()
    user_form = user_profile.applicationstatus.userform_set\
        .get(form__name__startswith=u'School report, CV and certifications')
    for field in user_form.form.fields.order_by('name'): # TODO: filter dictfields...
        data[ field.name ] = OrderedDict()
        for subject in sorted( user_form.form_data[ field.name ] ):
            if subject not in field.extra_options[u'mandatory_choices']:
                data[ field.name ][ subject ] = \
                    user_form.form_data[ field.name ][ subject ]
    return data

def _send_submission_email_to_user( user_profile ):
    _send_mail_to_user( 'submitted.html', user_profile )

def _send_submission_email_to_handler( user_profile, data_path, application_number ):
    _send_mail_to_handler( 'submitted.html', user_profile,
        context={'data_path':data_path, 'application_number':application_number} )

def _send_mail_to_handler( template, user_profile, context=None):
    context = context or {}
    context.update({'user_profile': user_profile})
    _send_mail_from_template(os.path.join('email/application_process/handler', template),
                             context, APPLICATIONPROCESS_HANDLER_EMAILS)
	
def _send_mail_to_user( template, user_profile, context=None):
    context = context or {}
    context.update({'user_profile': user_profile})
    _send_mail_from_template(os.path.join('email/application_process/user', template),
                             context, [user_profile.email])

def _send_mail_from_template( template, context, recipients ):
    mail_body = render_to_string( template, context )
    send_mail( APPLICATIONPROCESS_EMAIL_SUBJECT, mail_body, WEBVALLEY_EMAIL_ADDRESS, recipients, fail_silently=False)


########## FOR TESTING ###########
# but kept here, might be useful #

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from website.models import UserProfile
@login_required
@user_passes_test(lambda u: u.is_staff)
def json_summary(request, app_status_pk):
    user_profile = UserProfile.objects.get(applicationstatus__pk=app_status_pk)
    return HttpResponse( _get_json( _get_data( user_profile ) ), 
                         mimetype='application/json' )

@login_required
@user_passes_test(lambda u: u.is_staff)
def csv_summary(request, app_status_pk):
    user_profile = UserProfile.objects.get(applicationstatus__pk=app_status_pk)
    
    example = OrderedDict({"profile": "ciao",
                           "nonso": "bo"})
    
    res =  HttpResponse( _get_csv( _get_csv_data( user_profile ) ) ,
    #res =  HttpResponse( json.dumps( _get_csv_data( user_profile ), indent=4 ), 
                         #mimetype='text/plain' )
                         mimetype='text/csv' )
    res['Content-Disposition'] = 'attachment; filename=summary.csv'
    #with codecs.open( '/tmp/ciao.csv', 'w', encoding='utf-8' ) as data_file:
    #    data_file.write( _get_csv( _get_csv_data( user_profile ) ) )
    return res
