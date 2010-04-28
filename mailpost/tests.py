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

from mock import Mock, patch

from mailpost.imap import ImapClient, Message
from mailpost.handler import Handler, Mapper

string_message = '''from:TESTworldserveradministrator@TESTgoogle.com;
to:TESTlillianc@TESTgoogle.com;
subject:[AVAILABLE FOR TRANSLATION] A task in the WorldServer project '1271975280_109763_Geo Discussion;
 Forums - GDF UI sweep' is now in review.
=====
A task in the WorldServer project '1271975280_109763_Geo Discussion Forums - GDF UI sweep - locale: ru' is now in review.

=====;
'''

def return_string_message(*args, **kwargs):
    return 'OK', [ [[], string_message] ]
 
sessionmock = Mock()
sessionmock.uid = return_string_message

message = Message(session=sessionmock, uid=1)

MSG_LIST=[message, message]

sample_rules = [
        {
            'url': 'http://localhost:8000/mail_test/',
            'conditions': {
                'subject':  ['*AVAILABLE FOR TRANSLATION*',],
            },
            'add_params': {'message_type':'test'},
            'actions': ['mark_as_read'],
        },
        { #"Catch all" rule
            'url': 'http://localhost:8000/mail_test/',
        },
    ]

def test_mapper_current_workflow(*args, **kwargs):
   
    mapper = Mapper(sample_rules, 'http://localhost:8000')
    mapping = mapper.map(message)
    assert sample_rules[0]['conditions']['subject'][0] in mapping[1]\
        ['conditions']['subject'], mapping[1]['conditions']['subject']

def test_mapper_desired_workflow(*args, **kwargs):
    sample_rules_2 = sample_rules
    sample_rules_2[0]['conditions']['subject'][0] =\
         '\[AVAILABLE FOR TRANSLATION\]'
    mapper = Mapper(sample_rules_2, 'http://localhost:8000')
    mapping = mapper.map(message)
    assert sample_rules[0]['conditions']['subject'][0] in mapping[1]\
        ['conditions']['subject'], mapping[1]['conditions']['subject']

def test_fnmatch():
    from mailpost import fnmatch
    mypattern = '\[AVAILABLE FOR TRANSLATION\]'
    mystring = '[AVAILABLE FOR TRANSLATION] A task in the WorldServer project'
    assert fnmatch.fnmatch(mystring, mypattern)
        
