from django import forms
from models import AlumniStudent

class AlumniStudentForm(forms.ModelForm):
    name = forms.CharField(label="Name and Surname", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    loc_string = forms.CharField(label="Where do you live now?", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'autocomplete',
    }))
    email = forms.CharField(label="Current email (not published):", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    desc = forms.CharField(label="Short bio", widget=forms.Textarea(attrs={
        'placeholder': "Tell us your story!",
        'style': 'resize: vertical; width: 100%; height: 150px; min-height: 100px',
    }))
    year_in_school = forms.ChoiceField(label="Year of partecipation:", choices=((year, str(year)) for year in range(2001, 2018)),
                                       widget=forms.Select(attrs={
                                           'class': 'form-control'
                                       }))

    img = forms.ImageField(label="Picture of yourself", widget=forms.FileInput(attrs={
        'class': 'form-control-file',
        'type': 'image'
    }))
    lat = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'form-lat'}))
    lon = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'form-lon'}))

    class Meta:
        model = AlumniStudent
        fields = ['name', 'loc_string', 'email', 'desc', 'year_in_school', 'img', 'lat', 'lon']

    def clean_desc(self):
        return self.cleaned_data['desc'].strip()
    
    def clean_email(self):
        return self.cleaned_data['email'].strip()
    
    def clean_loc_string(self):
        return self.cleaned_data['loc_string'].strip()

class AlumniApprovalForm(forms.Form):
    id = forms.IntegerField()
    approved = forms.BooleanField(required=False)
