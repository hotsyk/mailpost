"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1
(C) 2010 oDesk www.oDesk.com
"""

import re
import urllib
import urllib2
import os
from imap import ImapClient
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers

from mailpost import fnmatch
from mailpost import auth

#TODO: Everything.

# This module is in 'works for now' stage
# Many features are missing and not all of existing features
# were decently tested
# You'd better stick to standard options for now

DEFAULT_RULE = {
    #Request params
    'method': 'post', #TODO: method is ignored for now
    'conditions': {},
    'syntax': 'glob',
    #Send message unparsed
    'raw': False,
    #Which message params to include in request
    'msg_params': ['from', 'sender', 'to', 'receiver', 'subject', 'body',
                   'date', 'Message-ID'],
    #Additional request params
    'add_params': {},
    'send_files': True,
    #Backend-specific actions
    'actions': [],
}


class ConfigurationError(Exception):
    pass


class Mapper(object):

    def __init__(self, mappings=None, base_url=None):
        self.base_url = base_url
        if not mappings:
            mappings = []
        self.mappings = mappings

    def map(self, message):
        for msg_rule in self.mappings:
            try:
                url = msg_rule['url']
            except KeyError:
                raise ConfigurationError('URL is required')
            if self.base_url:
                url = self.base_url.rstrip('/') + '/' + url.lstrip('/')
            rule = DEFAULT_RULE.copy()
            rule.update(msg_rule)
            match_func = fnmatch.fnmatch
            if rule['syntax'] == 'regexp':
                mathc_func = re.match
            match = True
            for key, pattern in rule['conditions'].items():
                value = message.get(key, None)
                if not value:
                    value = getattr(message, key, None)
                if not value:
                    match = False
                    break
                if type(pattern) in [list, tuple]:
                    match &= any([match_func(value, item) for item in pattern])
                elif isinstance(pattern, str):
                    match &= match_func(value, pattern)
                else:
                    raise ConfigurationError(\
                                "Pattern should be string or list, not %s" %\
                                             type(pattern))
            if match:
                return url, rule
        return None

    def process(self, inbox):
        """
        Inbox is expected to be a list of imap.Message objects.
        Although any list of mapping objects is accepted, provided
        that objects support methods enlisted in 'actions' option
        """

        # Poster: Register the streaming http handlers with urllib2
        register_openers()

        for message in inbox:
            res = self.map(message)
            if not res:
                continue
            url, options = res
            for action in options['actions']:
                getattr(message, action)()
            files = []
            if options['send_files']:
                for num, attachment in enumerate(message.attachments):
                    filename, ctype, fileobj = attachment
                    file_param = MultipartParam('attachment[%d]' % num,
                                                filename=filename,
                                                filetype=ctype,
                                                fileobj=fileobj)
                    files.append(file_param)
            data = {}
            for name in options['msg_params']:
                part = message.get(name, None)
                if not part:
                    part = getattr(message, name, None)
                if part: #TODO: maybe we should raise an exception
                         #if there's no part
                    data[name] = part
            data.update(options['add_params'])
            data = MultipartParam.from_params(data)
            data += files
            datagen, headers = multipart_encode(data)
            request = urllib2.Request(url, datagen, headers)
            if options.get('auth', None):
                cj, urlopener = auth.authenticate(options['auth'], request, 
                                                  self.base_url)
            try:
                result = urllib2.urlopen(request).read()
            except urllib2.URLError, e:
                result = e
                #continue    # TODO Log error and proceed.
            yield url, result


class Handler(object):

    def __init__(self, config=None, config_file=None, fileformat=None):
        """
        Either `config` or `config_file` must be pspecified
        `config` is a mapping that contains configuration options
        `config_file` is a name of configuration file
        If `fileformat` is absent, it will try to guess
        Possible values for `fileformat` are: 'yml'('yaml')
        """
        if not config:
            if not config_file:
                raise ValueError(\
                            "Either config or config_file must be specified")
            if not fileformat:
                fileformat = os.path.splitext(config_file)[1][1:]
            if fileformat in ['yml', 'yaml']:
                import yaml
                config = yaml.load(open(config_file, 'r'))
        self.config = config

    def load_backend(self):
        if self.config['backend'] == 'imap':
            host = self.config.get('host', None)
            if not host:
                raise ConfigurationError("'host' option is required")
            username = self.config.get('username', None)
            if not username:
                raise ConfigurationError("'username' option is required")
            password = self.config.get('password', None)
            if not password:
                raise ConfigurationError("'password' option is required")
            port = self.config.get('port', None)
            ssl = self.config.get('ssl', False)
            query = self.config.get('query', 'all')
            if not query in ['all', 'unseen', 'undeleted']:
                raise ConfigurationError("Unknown query: %s" % query)
            mailboxes = self.config.get('inboxes', ['INBOX'])
            self.base_url = self.config.get('base_url', None)

            self.rules = self.config['rules']
            client = ImapClient(host, username, password, port, ssl)
            self.msg_list = getattr(client, query)()
        else:
            raise ConfigurationError("Backend '%s' is not supported" %\
                                     self.config['backend'])

    def process(self):
        self.load_backend()
        mapper = Mapper(self.rules, self.base_url)
        for url, result in mapper.process(self.msg_list):
            yield url, result


if __name__ == '__main__':
    sample_rules = [
        {
            'url': 'http://localhost:8000/mail_test/',
            'conditions': {
                'sender': ['*@gmail.com', '*@odesk.com', '*@google.com'],
                'subject': '*test*',
            },
            'add_params': {'message_type':'test'},
            'actions': ['mark_as_read'],
        },
        { #"Catch all" rule
            'url': 'http://localhost:8000/mail_test/',
        },
    ]

    sample_config = {
        'backend': 'imap',
        'host': 'imap.gmail.com',
        'ssl': 'true',
        'username': 'clientg.test@gmail.com',
        'password': 'ClientGoogle',
        'rules': sample_rules,
    }

    handler = Handler(config=sample_config)
    handler.process()
