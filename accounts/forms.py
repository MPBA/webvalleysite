from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Last name'))
    mail = forms.EmailField(max_length=40, required=True, label=_('E-mail'))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(render_value=False),
                                label=_('Password'))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(render_value=False),
                                label=_('Confirm password'))
    captcha = ReCaptchaField()
    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields['first_name'].widget.attrs.update({'class' : 'form_group'})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_mail(self):
        """
        Normalize mail like django's models.BaseUserManager
        """
        email = self.cleaned_data.get('mail')
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])

        form_email = email
        try:
            u = User.objects.get(email=form_email)
        except User.DoesNotExist:
            return form_email
        raise validators.ValidationError('Email "{email}" is already taken.'.format(email=form_email))
