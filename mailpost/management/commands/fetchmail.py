import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from mailpost.handler import Handler

class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DISABLE_FETCHMAIL:
            print "Fetchmail is disabled"
            return False
        if os.path.exists(settings.LOCK_FILENAME):
            print "Lock file found! Cannot run another process."
            print "If you believe this is a mistake," + \
                  " please delete '%s' file manually" % \
                  os.path.normpath(settings.LOCK_FILENAME)
            return False

        handler = Handler(config_file=settings.MAILPOST_CONFIG_FILE)

        f = open(settings.LOCK_FILENAME,'w')
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
