"""
A package that maps incoming email to HTTP requests
Mailpost version 0.0.1 alpha
(C) 2010 OTT Team
"""

import imaplib
import email
from cStringIO import StringIO
import re

#WARNING: This module is at very early stage of development

#Simplicity and ease of use of the API were chosen over techical correctness
#and perfrormance.
#The goal is to provide an API that is closer to user's perspective than to
#formal standards

#TODO: Lot's of stuff
# Most important
# 1. Dates!!
# 2. Download only headers of a message until body or attachments are 
# requested
# 3. Encodings support

SENDER_EXPR = re.compile(r'[\w\.]+@[\w\.-]+') #Doesn't care for email validity much

class Message(object):
    
    def __init__(self, session, uid):
        self.session = session
        self.uid = uid
        status, data = self.session.uid('FETCH', uid, '(RFC822)')
        #status, data = self.session.uid('FETCH', uid, '(BODYSTRUCTURE)')
        if status != 'OK':
            raise Exception(data)
        self._msg = email.message_from_string(data[0][1])
        self._prepare()

    def _prepare(self):
        self.text_bodies = []
        self.html_bodies = []
        self.attachments = []
        self.sender = ''
        self.receiver = ''
        sender = SENDER_EXPR.search(self._msg['from'])
        if sender:
            self.sender = sender.group()
        receiver = SENDER_EXPR.search(self._msg['to'])
        if receiver:
            self.receiver = receiver.group()
        for part in self._msg.walk():
            filename = part.get_filename()
            ctype = part.get_content_type()
            if filename:
                self.attachments.append((filename, ctype, 
                                         StringIO(part.get_payload(decode=True))))
            else:
                if ctype == 'text/plain':
                    self.text_bodies.append(part.get_payload())
                elif ctype == 'text/html':
                    self.html_bodies.append(part.get_payload())

    def __getitem__(self, name):
        return self._msg[name]

    def __contains__(self, name):
        return self.has_key(name)

    def has_key(self, name):
        return self._msg.has_key(name)
    
    def get(self, name, failobj=None):
        return self._msg.get(name, failobj)
    
    def __str__(self):
        headers = ("From   : %(from)s\n-----\nTo     : %(to)s\n" +
        "-----\nSubject: %(subject)s\n") % self._msg
        return "%s=====\n%s\n=====\n\n" % (headers, self.body)

    @property
    def body(self):
        return "\n".join(self.text_bodies)

    def add_flag(self, flag):
        self.session.uid('STORE', self.uid, '+FLAGS', flag)

    def mark_as_read(self):
        self.add_flag(r'\Seen')

    def delete(self):
        self.add_flag(r'\Deleted')

    def download(self):
        #TODO: Ideally we shouldn't download the whole thing in order to parse 
        #headers. 
        pass



class MessageList(object):

    def __init__(self, session, query):
        self.session = session
        self.query = query
        self._cache = {}
        self._uids = None

    def _get_uids(self):
        charset = None #FIXME
        status, data = self.session.uid('SEARCH', charset, self.query)
        if status != 'OK':
            raise Exception(data)
        self._uids = data[0].split()

    def __len__(self):
        if self._uids is None:
            self._get_uids()
        return len(self._uids)

    def __iter__(self):
        if self._uids is None:
            self._get_uids()
        for uid in self._uids:
            yield self.get(uid)

    def __getitem__(self, key):
        if not isinstance(key, (slice, int)):
            raise TypeError
        if self._uids is None:
            self._get_uids()
        if isinstance(key, slice):
            #TODO: Generator should be used here:
            return [self.get(uid) for uid in self._uids[key]]
        else:
            return self.get(self._uids[key])

    def get(self, uid):
        return self._cache.get(uid, Message(self.session, uid))


class ImapClient(object):

    headers_format = '(RFC822)'

    def __init__(self, host, username, password, port=None, ssl=False):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssl = ssl
        self._connection = None
        self.logged_in = False
        self.mailbox = None
        self.echo = False

    def connect(self):
        if self.ssl:
            default_port = 993 
            cls = imaplib.IMAP4_SSL
        else:
            default_port = 143 
            cls = imaplib.IMAP4
        port = self.port or default_port
        self._connection = cls(self.host, port)
    
    @property
    def connection(self):
        if not self._connection:
            self.connect()
        return self._connection

    def login(self, username, password):
        self.connection.login(username,password)

    def select(self,mailbox='INBOX'):
        if not self.logged_in: #TODO: Maybe general 'state' would be better
            self.login(self.username, self.password)
        if self.mailbox:
            self.connection.close()
        self.connection.select(mailbox)
        self.mailbox = mailbox

    def search(self, query):
        if not self.mailbox:
            self.select()
        return MessageList(self.connection, query)

    def all(self):
        return self.search('ALL')

    def unseen(self):
        return self.search('UNSEEN')

    def nondeleted(self):
        return self.search('(NOT DELETED)')

    def deleted(self):
        return self.search('(DELETED)')

    def close(self):
        self.connection.close()
        self._connection = None

    def logout(self):
        self.close()
        self.connection.logout()


if __name__ == '__main__':
    USERNAME = 'clientg.test@gmail.com'
    PASSWORD = 'ClientGoogle' 
    inbox = ImapClient('imap.gmail.com', USERNAME, 
                       PASSWORD, ssl=True) 
    print '---- LATEST 10 messages ----'
    for message in inbox.nondeleted()[-10:]:
        print message
    inbox.logout()