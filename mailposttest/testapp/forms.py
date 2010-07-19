"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1
(C) 2010 oDesk www.oDesk.com
"""


import logging
import re

from django import forms


class EmailForm(forms.Form):
    sender = forms.CharField(required=False)
    to = forms.CharField(required=False)
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)
