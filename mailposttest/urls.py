from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('mailposttest.testapp.views',
    url(r'^upload_email/$', 'upload_email',
        name='upload_email'),
    url(r'^accounts/login/$', 'login',
        name='login'),
        
)
