from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from djrichtextfield.widgets import RichTextWidget

class CandidateForm(forms.ModelForm):
    class Meta:
        exclude = ('user',)
        model = Candidate
        fields="__all__"