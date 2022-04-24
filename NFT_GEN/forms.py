from django.core import validators
from django import forms
from .models import ProjectDesc

class ProjRegistration(forms.ModelForm):
    class Meta:
        model = ProjectDesc
        fields = ['proj_name','total']
        widgets = {
            'proj_name':forms.TextInput(attrs={'class':'form-control'}),
            'total':forms.TextInput(attrs={'class':'form-control'}),
        }