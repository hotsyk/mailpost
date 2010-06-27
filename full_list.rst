.. _full_list:


********************************
Full list of classes and methods
********************************

.. 
.. _exceptions:

Exceptions
------------

* handler.py 

 * class ConfigurationError(Exception)

..
.. _auth:

auth.py
-----------------

* def get_handlers()
 
 * Get handlers registered by the poster.streaminghttp.register_openers, as we are overriding them by adding 2 new handlers

* def authenticate(auth_data, request)
 
 * Format for auth_data::
 
    url: <url to login form> 
    form:
      username (name of the field in POST): value
      passwd (name of the field in POST): value
 
.. _fnmatch:

fnmatch.py
------------------------------------
Fork of original fnmatch

..
.. _purpose:

Purpose of the fork
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Original fnmatch has an issue while matching escaped strings and not match
pattern in the string, just only complete match. To support in glob syntax 
same rules as we support in regex, we've decided to fork it and patch

..
.. _description:

Original descripition of fnmatch 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)

..
.. _methods:

Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* def fnmatch(name, pat)
 
 * Test whether FILENAME matches PATTERN
 
* def filter(names, pat)

 * Return the subset of the list NAMES that match PAT
 
* def fnmatchcase(name, pat)
 
 * Test whether FILENAME matches PATTERN, including case.
 
* def translate(pat)
 
 * Translate a shell PATTERN to a regular expression
 * Patched to quote meta characters

..
.. _handler:

handler.py
------------------------------------

* class Mapper(object)
 
 * def __init__(self, mappings=None, base_url=None)
 * def map(self, message)
 * def process(self, inbox)

* class Handler(object)

 * def __init__(self, config=None, config_file=None, fileformat=None)
 * def load_backend(self)
 * def process(self)

..
.. _imap:

imap.py
------------------------------------

* class Message(object)

 * def __init__(self, session, uid)
 * def _prepare(self)
 * def __getitem__(self, name)
 * def __contains__(self, name)
 * def has_key(self, name)
 * def get(self, name, failobj=None)
 * def __str__(self)
 * @property def body(self)
 * def add_flag(self, flag)
 * def mark_as_read(self)
 * def delete(self)
 * def download(self)
 
* class MessageList(object)

 * def __init__(self, session, query)
 * def _get_uids(self)
 * def __len__(self)
 * def __iter__(self)
 * def __getitem__(self, key)
 * def get(self, uid)
 
* class ImapClient(object)

 * def __init__(self, host, username, password, port=None, ssl=False)
 * def connect(self)
 * @property def connection(self)
 * def login(self, username, password)
 * def select(self, mailbox='INBOX')
 * def search(self, query)
 * def all(self)
 * def unseen(self)
 * def nondeleted(self)
 * def deleted(self)
 * def close(self)
 * def logout(self)

..
.. _tests:

tests.py
------------------------------------

* class TestFnmatch(unittest.TestCase)

 * def check_match(self, filename, pattern, should_match=1)
 * def check_translate(self, sample, pattern, should_match=1)
 * def test_fnmatch

* class TestMailPost(unittest.TestCase)

 * def test_mapper_current_workflow
 * def test_mapper_desired_workflow
 * def test_message_id
 
..
.. _management:

management/commands/fetchmail.py
------------------------------------

* class Command(BaseCommand)
 
 * def handle 
