from datetime import date
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from website.models import UserProfile

from models import ApplicationStatus, UserForm


class ApplicationProcessSelectForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatus
        fields = ['application_process']

    def __init__(self, *args, **kwargs):
        super(ApplicationProcessSelectForm, self).__init__(*args, **kwargs)
        self.fields['application_process'].required = True

    def clean_application_process(self):
        data = self.cleaned_data['application_process']
        today = date.today()
        if today > data.deadline:
            raise ValidationError(_(u'Applications are closed for the selected application process. If you encountered some problems during your submission please contact us webvalley@fbk.eu'))
        elif today < data.start:
            raise ValidationError(_(u'We are not accepting any applications for this application process yet. Applications will start on ') + str(data.start))
        return data

    def save(self, user):
        application_process = self.cleaned_data['application_process']
        user_profile = UserProfile.objects.get_or_create( user=user )[0]
        a = ApplicationStatus( application_process=application_process,
            user_profile=user_profile)
        a.save()

class UploadSignedCopyForm(forms.ModelForm):
    class Meta:
        model = UserForm
        fields = ['signed_copy']

    def __init__(self, *args, **kwargs):
        super(UploadSignedCopyForm, self).__init__(*args, **kwargs)
        self.fields['signed_copy'].required = True
    
#    def clean_signed_copy(self):
#        accepted_half_mimes = ['image'] # like 'image/*'
#        accepted_whole_mimes = ['application/pdf']
#        error_message = _(u'The file must be either an image or a pdf file.')
#        file = self.cleaned_data['signed_copy']
#        import magic
#        mimegen = magic.Magic(mime=True)
#        mime = mimegen.from_buffer(file.read(1024)) # TODO: is this enough?
#        wholemime = mime.split(';')[0]
#        halfmime = wholemime.split('/')[0]
#        condition = ( (halfmime in accepted_half_mimes)
#                      or (wholemime in accepted_whole_mimes) )
#        #with open('debug','a') as debug:
#        #    print >>debug, mime
#        #    print >>debug, wholemime
#        #    print >>debug, halfmime
#        #    print >>debug, condition
#
#        if not condition:
#            raise forms.ValidationError(error_message)
#        # Always return the cleaned data.
#        return file

