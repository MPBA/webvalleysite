from os.path import join

from django.db import models
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

import jsonfield

from website.models import UserProfile

from applicationprocess_settings import USER_DATA_ROOT, FormStatusChoices

APPLICATION_STATUS_OPTIONS = (
    ( u'S_SUB' ,_( 'Submitted' )),
    ( u'S_IPR', _( 'In progress' )),
#    ( u'S_ERR', _( 'With errors' )),
)

class FieldType( models.Model ):
    @property
    def name(self):
        return self.target_class.split( '.' )[-1]

    target_class = models.CharField(max_length=255,
        help_text=_("It must be a complete package name (such as foo.bar.myfield)"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Field type')
        verbose_name_plural = _('Field types')

class ValidatorType( models.Model ):
    @property
    def name(self):
        return self.target_class.split( '.' )[-1]

    target_class = models.CharField(max_length=255,
        help_text=_("It must be a complete package name (such as foo.bar.myvalidator)"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Validator type')
        verbose_name_plural = _('Validator types')


class Validator( models.Model ):
    name = models.CharField(max_length=255)
    type = models.ForeignKey( ValidatorType )
    options = jsonfield.JSONField( default='{}', blank=True,
        help_text=_("Options that will be passed to the validator __init__ method."))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Validator')
        verbose_name_plural = _('Validators')

class Field( models.Model ):
    name = models.CharField(max_length=255, unique=True)
    label = models.CharField( max_length=255 )
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey( FieldType )
    validators = models.ManyToManyField( Validator, blank=True, null=True)
    required = models.BooleanField(default=True)
    extra_options = jsonfield.JSONField( default='{}', blank=True,
                    help_text=_("Extra options that will be passed to the field __init__ method."))
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')

class Form( models.Model ):
    name = models.CharField(max_length=255, unique=True)
    fields = models.ManyToManyField( Field )
    description = models.TextField( blank=True, null=True )
    upload_required = models.BooleanField(default=True, help_text=_(
        _("Whether the form will completed with a file-upload field for a signed copy of the form itself.")))

    _get_upload_to_templates = (lambda instance, filename: join(
            "form-templates",
            instance.name + ".html"))

    template = models.FileField(upload_to=_get_upload_to_templates, blank=True, null=True)

    _get_upload_to_templates = (lambda instance, filename: join(
        "blank-forms",
        filename))

    blank_form = models.FileField(upload_to=_get_upload_to_templates, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')

class ApplicationProcess( models.Model ):
    name = models.CharField(unique=True, max_length=255, help_text=_("Refer to the WebValley announcement document"))
    forms = models.ManyToManyField( Form, through='ApplicationProcessForm' )

    start = models.DateField(_(u'Application start'))
    deadline = models.DateField(_(u'Application deadline'))

    def clean(self):
        # Don't allow deadline to be before start
        if self.start > self.deadline:
            raise ValidationError(_(u'It is not appropriate for the deadline to come before the application start date'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Application process')
        verbose_name_plural = _('Application processes')

# Many to many intermediate table
class ApplicationProcessForm( models.Model ):
    application_process = models.ForeignKey( ApplicationProcess )
    form = models.ForeignKey( Form )
    index = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super( ApplicationProcessForm, self ).__init__( *args, **kwargs )
        # Every time an instance of this class gets created (every time a new
        # record is added to this table) the correspondent UserForm is added
        # to every user who has the same ApplicationProcess

    def __unicode__(self):
        return u"{application_process} : {form}".format(
            application_process=self.application_process.name,
            form=self.form.name
        )

    class Meta:
        unique_together = (( 'application_process', 'form' ), )

    def save(self):
        with transaction.atomic():  # Hopefully, this is a serializable transaction
            # read from database the current status of this object (if self.pk is not null)
            # compare what was read with self
            # Take proper action, basing on the diff (new item/index chanded/s.t. important changed)
            # TODO: move the signal handler to here
            super(ApplicationProcessForm, self).save()

class ApplicationStatus( models.Model ):
    status = models.CharField( max_length=5,
                               choices=APPLICATION_STATUS_OPTIONS,
                               blank = True,
                               default='S_IPR' )
    user_profile = models.OneToOneField( UserProfile, unique=True )
    application_process = models.ForeignKey( ApplicationProcess )

    def ready_for_submission(self):
        ret = self.user_profile.filled_for_application
        for form in self.userform_set.all():
            ret = ret and form.is_completed
        return ret

    def __unicode__(self):
        return u"{user} : {application_process}"\
            .format(user=self.user_profile.full_name,
                    application_process=self.application_process.name )

    class Meta:
        verbose_name = _( 'Application status' )
        verbose_name_plural = _( 'Application statuses' )

class UserForm( models.Model ):
    form = models.ForeignKey( Form )
    application_status = models.ForeignKey( ApplicationStatus )
    form_data = jsonfield.JSONField( blank=True, default='{}')

    _get_upload_to = lambda instance, filename:join(
        'docs', instance.application_status.user_profile.user.username,
        'signed-forms', instance.form.name + u'.' + filename.split('.')[-1])

    signed_copy = models.FileField( upload_to=_get_upload_to, blank=True, null=True )
    
    class Meta:
        unique_together = (( 'application_status', 'form' ), )

    @property
    def description(self):
        return self.form.description

    @property
    def is_filled(self):
        #form_class_object = FormFactory.form_from_user_form( self )
        #bound_form = form_class_object( self.form_data )
        #return bound_form.is_valid_from_cleaned_data()

        return bool( self.form_data <> '{}' )
        # return bool(self.form_data)

    @property
    def is_completed(self):
        # Need to check if there is a better way to check if the file is really there.
        return self.is_filled and (self.signed_copy or (not self.form.upload_required))

    @property
    def status(self):
        if self.is_completed:
            return FormStatusChoices.COMPLETED
        elif self.is_filled:
            return FormStatusChoices.FILLED
        else:
            return FormStatusChoices.INCOMPLETE

    @property
    def index(self):
        return ApplicationProcessForm.objects.get( form=self.form,
            application_process=self.application_status.application_process).index

    @property
    def blank_form_url(self):
        retval = self.form.blank_form
        if retval:
            return retval.url
        return None

    def __unicode__(self):
        return u"{user} : {form_name}".format(
            user=self.application_status.user_profile.full_name,
            form_name=self.form.name )




# Handle here the event of the association of a form object with a signup process
# (i.e. every user who has that signup process gets a new UserForm object)
@receiver( post_save, sender=ApplicationProcessForm, weak=False, dispatch_uid="assign_new_form")
def assign_new_form_to_users( sender, **kwargs ):
    if(kwargs.get( 'created' )):
        application_process = kwargs.get( 'instance' ).application_process
        new_form = kwargs.get( 'instance' ).form
        affected_application_statuses = application_process.applicationstatus_set.all()

        with transaction.atomic():
            for current_application_status in affected_application_statuses:
                new_user_form = UserForm( form=new_form,
                    application_status=current_application_status )
                new_user_form.save()
# TODO: DELETE AND RECREATE RELATED USER FORMS
# TODO: Handle change of application process.
# TODO: FIX SIGNALS AS DISCUSSED WITH DAVIDE (ROBERTO)

# I couldn't find in the whole django documentation one line stating whether
# the pre_save signal is or is not executed in the same transaction with save, 
# thus I will assume it is not, thus I will override the save() method itself.
# One never knows, transactions might save your ass

# Handle here the event of a new user starting an application process.
# In case a user gets deleted the cascade clause in the db will do the job.
@receiver( post_save, sender=ApplicationStatus, weak=False, dispatch_uid="assign_userform_to")
def assign_userforms_to_new_user( sender, **kwargs ):
    if(kwargs.get( 'created' )): # Anche qui sarebbe meglio fare controlli piu` profondi, ma per ora potrebbe bastare
        application_status = kwargs.get( 'instance' )
        application_process = application_status.application_process
        form_list = application_process.forms.all()

        with transaction.atomic():
            for current_form in form_list:
                new_user_form = UserForm( application_status=application_status,
                    form=current_form)
                new_user_form.save()
    

