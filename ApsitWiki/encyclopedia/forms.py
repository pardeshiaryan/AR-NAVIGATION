# encyclopedia/forms.py

from django import forms
from .models import Page

class NewPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content']
