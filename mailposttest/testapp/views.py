"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1
(C) 2010 oDesk www.oDesk.com
"""


from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, \
                        HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test

from mailposttest.testapp.forms import *


@user_passes_test(lambda u: u.is_staff)
def upload_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            context = {'status': 'ok'}
            return render_to_response('email_form.html',
                              RequestContext(request, context))
        context = {'status': 'error', 'form': form}
        return render_to_response('email_form.html',
                              RequestContext(request, context))
    else:
        form = EmailForm()
        context = {'form': form}
        return render_to_response('email_form.html',
                              RequestContext(request, context))
