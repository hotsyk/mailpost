import logging
import re

from django import forms

class EmailForm(forms.Form):
    sender = forms.CharField()
    to = forms.CharField()
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)


