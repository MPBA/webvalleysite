from os.path import join

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from validators import validate_country_code


GENDER_CHOICES = (('M', _('Male')),('F', _('Female')))
# TODO: Documentation

class Country(models.Model):
    name = models.CharField(_('name'), max_length=30)
    # http://www.i18nguy.com/unicode/language-identifiers.html
    language_identifier = models.CharField(_('language identifier'), max_length=5, validators=[validate_country_code])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

class UserProfile(models.Model):
    # User implementation is provided by the auth plugin of django :
    user = models.OneToOneField( User )
    # Nationality of the user :
    nationality = models.ForeignKey(Country, blank=True, null=True, verbose_name=_('nationality'))
    # General information :
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(_('birth date'), help_text=u'mm/dd/yyyy', blank=True, null=True)
    birth_place = models.CharField(_('birth place'), max_length=30, blank=True, null=True)
    #home_phone = models.IntegerField(_('home phone'), blank=True, null=True)
    #mobile_phone = models.IntegerField(_('mobile phone'), blank=True, null=True)
    home_phone = models.CharField(_('home phone'), max_length=30, blank=True, null=True)
    mobile_phone = models.CharField(_('mobile phone'), max_length=30, blank=True, null=True)
    # Photo :
    _get_upload_to = lambda instance, filename: join(
        'docs', instance.user.username, 'profile.' + filename.split('.')[-1])
    photo = models.ImageField(verbose_name=_('photo'), upload_to=_get_upload_to, blank=True, null=True)

    # If this is set to true the image and brief bio
    # are displayed into the page of "The team"
    # Note : being staff does NOT require the user to be a past webvalley
    # participant.
    is_webvalley_staff = models.BooleanField(_('webvalley staff member ?'), default=False)

    #application_status = models.OneToOneField( ApplicationStatus,
    #null=True, blank=True)

    # User Registration: activation key and key expiration date
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)

    @property
    def first_name( self ):
        return self.user.first_name

    @property
    def last_name( self ):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return u"{first_name} {last_name}".format( first_name=self.first_name, last_name=self.last_name )

    # Fields that need not to be blank in order to complete application to the school
    _application_needed_fields = ["nationality",
                                 "gender",
                                 "birth_date",
                                 "birth_place",
                                 "home_phone",
                                 "mobile_phone",
                                 "photo"]

    def filled_for_application(self):
        for field_name in self._application_needed_fields:
            if not getattr( self, field_name, False ):
                return False
        return True

    def __unicode__( self ):
    # Just for development, in normal user registration first and last name will be mandatory.
        if self.user.first_name and self.user.last_name:
            return self.full_name
        else:
            return self.user.username

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

