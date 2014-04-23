import datetime
from django import forms
from website.models import UserProfile


class EditProfileForm(forms.ModelForm): # God bless ModelForms!
    birth_date = forms.DateField( required=False,
                                  initial=datetime.date(1990, 01, 01), widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}))
    birth_place = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}))
    home_phone = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}))
    mobile_phone = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}))

    class Meta:
        model = UserProfile
        fields = ('gender', 'nationality', 'birth_date', 'birth_place', 'home_phone', 'mobile_phone', 'photo')
        widgets = {'birth_date': forms.Textarea(attrs={'id':'id_birth_date'}),}

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].help_text = self._meta.model._meta.get_field("birth_date").help_text
