from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate,SampleLanguageCodes
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from djrichtextfield.widgets import RichTextWidget
from djangoeditorwidgets.widgets import MonacoEditorWidget

class CandidateForm(forms.ModelForm):
    class Meta:
        exclude = ('user',)
        model = Candidate
        fields="__all__"

class SampleLanguageCodeForm(forms.ModelForm):
    class Meta:
        model = SampleLanguageCodes
        fields="__all__"
        widgets = {
            "code": MonacoEditorWidget(
                attrs={"data-wordwrap": "on", "data-language": "javascript"}
            )
        }