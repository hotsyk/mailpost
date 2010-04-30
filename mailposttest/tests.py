"""
Mailpost version 0.0.1 alpha
(C) 2010 OTT Team

"""

import re
import urllib
import urllib2
import os
import imaplib
import email
from cStringIO import StringIO

import unittest
from mock import Mock, patch

from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler

from mailpost.fnmatch import fnmatch, fnmatchcase, translate
from mailpost.imap import ImapClient, Message
from mailpost.handler import Handler, Mapper
from mailpost.tests import TestMailPost

data = {'sender': 'sender',
          'subject': 'subject',
          'to': 'to',
          'body': 'body'}  

class TestMailPostAuthentication(TestMailPost):
    
    def __init__(self, *args, **kwargs):
        super(TestMailPostAuthentication, self).__init__(*args, **kwargs)
        for user in User.objects.all():
            user.delete()
        self.user = User.objects.create_user('john', 'test@test.com', 'pass')
        self.user.is_staff = True
        self.user.save()
        
        self.sample_config = {'backend': 'imap',
                              'host': 'imap.gmail.com',
                              'ssl': 'true',
                              'username': 'test@gmail.com',
                              'password': 'test',
                              'mailboxes': ['INBOX'],
                              'query': 'all',
                              'base_url': 'http://localhost:8000/',
                              'rules': self.sample_rules}
        
    def test_authentication_on_form(self):
      
        client = Client()
        response = client.post('/upload_email/', data)
        assert not 'ok' in response.content, response.content
        request = client.request()
        client.login(username='john', password='pass')
        response = client.post('/upload_email/', data)
        assert 'ok' in response.content, response.content

    def test_mailpost_with_auth(self):
        """
        auth:
        form:
            username: 'john'
            passwd: 'pass'
        """
        import urllib2
        from servertest import *
        self.sample_rules[0]['auth'] = {'form': {'username': 'john', 
                                                 'passwd': 'pass'}}
        server = TestServerThread("127.0.0.1", 8082)
        server.start()
        results = []
        try:
            mapper = Mapper(self.sample_rules, 
                        'http://127.0.0.1:8082')
            for url, result in mapper.process(self.msg_list):
                results.append([url, result])
        except Exception, e:
            server.stop()
            raise e  
        server.stop()
        assert not ('Login' in results[0][1]), results[0][1]
        assert ('OK' in results[0][1]), results[0][1]
        
        