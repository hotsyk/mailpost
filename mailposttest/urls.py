"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1.0 alpha
(C) 2010 oDesk www.oDesk.com
"""

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('mailposttest.testapp.views',
    url(r'^upload_email/$', 'upload_email',
        name='upload_email'),
    url(r'^admin/', include(admin.site.urls)),
        
)

def login(request):
    from django.contrib.auth.views import login as auth_login
    return auth_login(request, template_name='admin/login.html')
    
urlpatterns += patterns('',
    url(r'^login/$', login, name='login',),
    url(r'^accounts/login/$', login, name='login2',),
)    
