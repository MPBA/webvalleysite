from django import forms
from models import AlumniStudent

class AlumniStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    loc_string = forms.CharField(label="Where do you live now?", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'autocomplete',
    }))
    desc = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        'placeholder': "Tell us your story!",
        'style': 'resize: vertical; width: 100%; height: 150px; min-height: 100px',
    }))
    year_in_school = forms.ChoiceField(choices=((year, str(year)) for year in range(2001, 2017)),
                                       widget=forms.Select(attrs={
                                           'class': 'form-control',
                                           'style': 'display: inline-block; width: 100px; margin-left: 5px; margin-right: 50px;'
                                       }))

    img = forms.ImageField(label="Picture of yourself", widget=forms.FileInput(attrs={
        'class': 'form-control-file',
        'style': 'display: inline-block; margin-left: 5px;',
        'type': 'image'
    }))
    lat = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'form-lat'}))
    lon = forms.FloatField(widget=forms.HiddenInput(attrs={'id': 'form-lon'}))

    class Meta:
        model = AlumniStudent
        fields = ['name', 'loc_string', 'desc', 'year_in_school', 'img', 'lat', 'lon']
