"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1.0 alpha
(C) 2010 oDesk www.oDesk.com
"""


import re
import urllib
import urllib2
import os
import imaplib
import email
from cStringIO import StringIO

import unittest
from mock import Mock

from mailpost.fnmatch import fnmatch, fnmatchcase, translate
from mailpost.imap import ImapClient, Message
from mailpost.handler import Handler, Mapper


class TestFnmatch(unittest.TestCase):

    def check_match(self, filename, pattern, should_match=1):
        if should_match:
            self.assert_(fnmatch(filename, pattern),
                         "expected %r to match pattern %r"
                         % (filename, pattern))
        else:
            self.assert_(not fnmatch(filename, pattern),
                         "expected %r not to match pattern %r"
                         % (filename, pattern))

    def check_translate(self, sample, pattern, should_match=1):
        if should_match:
            self.assert_(translate(pattern) == sample + '\Z(?ms)',
                         "expected %r to match pattern %r"
                         % (sample, pattern))
        else:
            self.assert_(not translate(pattern) == sample + '\Z(?ms)',
                         "expected %r not to match pattern %r"
                         % (sample, pattern))

    def test_fnmatch(self):
        check = self.check_match
        check('abc', 'abc')
        check('abc', '?*?')
        check('abc', '???*')
        check('abc', '*???')
        check('abc', '???')
        check('abc', '*')
        check('abc', 'ab[cd]')
        check('abc', 'ab[!de]')
        check('abc', 'ab[de]', 0)
        check('a', '??', 0)
        check('a', 'b', 0)

        # these test that '\' is handled correctly in character sets;
        check('\\', r'[\]')
        check('a', r'[!\]')
        check('\\', r'[!\]', 0)

        # these test that escaping works
        check('[test]', r'\[test\]')
        check('[$%^est]', r'\[\$\%\^est\]')
        check('a*c', '?\*?')
        check('a?bc', '?\??*')
        check('ab??c', '*\?\??')
        check('*abc', '\**')
        check('abd', 'ab[de]')
        check('abc', 'a\[bc', 0)
        #when we escape only ], it handled as usual in glob - [] rule
        check('abd', 'ab[de\]', 1)
        check('abda', 'ab[de\]?', 1)
        #when we escape only [ - it works as escaped for both
        check('ab[de]', 'ab\[de]', 1)
        check('abd', 'ab\[de]', 0)

        #check some rules directly using fnmatch.translate
        check = self.check_translate
        check('\[\$\%\^est\]', r'\[\$\%\^est\]')
        check('\*\*', '\*\*')
        check('\*\[[*]', '\*[*]', 0)

string_message = '''from:TESTserveradministrator@gmail.com;
to:TESTlillianc@gmail.com;
subject:[AVAILABLE FOR TRANSLATION] A task in our server
Message-ID:123
project 'New project;
 Test - test2' is now available to review
=====
A task in our server project 'New project;
 Test - test2' is now available to review
=====;
'''


class TestMailPost(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        def return_string_message(*args, **kwargs):
            return 'OK', [[[], string_message]]

        super(TestMailPost, self).__init__(*args, **kwargs)

        self.sessionmock = Mock()
        self.sessionmock.uid = return_string_message

        self.message = Message(session=self.sessionmock, uid=1)

        self.msg_list = [self.message, self.message]

        self.sample_rules = [
                {
                    'url': '/upload_email/',
                    'conditions': {
                        'subject': ['*AVAILABLE FOR TRANSLATION*', ],
                    },
                    'add_params': {'message_type':'test'},
                    'actions': ['mark_as_read'],
                },
                { #"Catch all" rule
                    'url': '/upload_email/',
                },
            ]

    def test_mapper_current_workflow(self, *args, **kwargs):

        mapper = Mapper(self.sample_rules, 'http://localhost:8000')
        mapping = mapper.map(self.message)
        self.assert_(self.sample_rules[0]['conditions']['subject'][0]\
                      in mapping[1]['conditions']['subject'],
                      mapping[1]['conditions']['subject'])

    def test_mapper_desired_workflow(self, *args, **kwargs):
        sample_rules_2 = self.sample_rules
        sample_rules_2[0]['conditions']['subject'][0] =\
             '\[AVAILABLE FOR TRANSLATION\]*'
        mapper = Mapper(sample_rules_2, 'http://localhost:8000')
        mapping = mapper.map(self.message)
        self.assert_(self.sample_rules[0]['conditions']['subject'][0]\
                      in mapping[1]['conditions']['subject'],
                      mapping[1]['conditions']['subject'])

    def test_message_id(self, *args, **kwargs):

        mapper = Mapper(self.sample_rules, 'http://localhost:8000')
        mapping = mapper.map(self.message)
        assert 'Message-ID' in mapping[1]['msg_params']
