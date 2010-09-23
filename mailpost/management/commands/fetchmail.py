"""
A package that maps incoming email to HTTP requests
Mailpost version 0.1
(C) 2010 oDesk www.oDesk.com
"""


import os, datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.mail import mail_admins

from mailpost.handler import Handler

class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DISABLE_FETCHMAIL:
            print "Fetchmail is disabled"
            return False
        if os.path.exists(settings.LOCK_FILENAME):
            statinfo = os.stat(os.path.normpath(settings.LOCK_FILENAME))
            last_file_lock_time = \
                datetime.datetime.fromtimestamp(statinfo.st_ctime)
            duration = datetime.datetime.now() - last_file_lock_time
            if duration > datetime.timedelta(minutes = \
                10 * settings.LOCK_FILE_MAIL_ADMIN_CONSECUTIVE_NUMBER):
                print "Lock file found! Cannot run another process."
                print "If you believe this is a mistake," + \
                      " please delete '%s' file manually" % \
                      os.path.normpath(settings.LOCK_FILENAME)
                mail_admins('MAILPOST:Lock file found!'+\
                            ' Cannot run another process',\
                            "If you believe this is a mistake," + \
                            " please delete '%s' file manually" % \
                            os.path.normpath(settings.LOCK_FILENAME),
                            fail_silently=True)
            return False

        handler = Handler(config_file=settings.MAILPOST_CONFIG_FILE)

        f = open(settings.LOCK_FILENAME, 'w')
        f.close()
        try:
            for url, result in handler.process():
                print 'Sent to URL: %s' % url
                if isinstance(result, Exception):
                    print 'Error: ', result
                else:
                    print 'OK'
        finally:
            os.remove(settings.LOCK_FILENAME)
