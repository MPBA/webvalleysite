from django import forms
from models import AlumniStudent

class AlumniStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    loc_string = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.Textarea()
    img = forms.ImageField(required=True)


    class Meta:
        model = AlumniStudent
        fields = ['name', ]
