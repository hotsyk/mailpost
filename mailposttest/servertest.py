"""
Threading server to test urllib2.urlopen

A package that maps incoming email to HTTP requests
Mailpost version 0.1
(C) 2010 oDesk www.oDesk.com
"""



import BaseHTTPServer
import SocketServer
import random
import time
import threading
import urllib

from django.core.servers import basehttp
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler
from django.core.handlers.wsgi import WSGIHandler


class RandomWaitMixin(object):

    def process_request(self, *args, **kwargs):
        time.sleep(random.random() / 3)
        return super(RandomWaitMixin, self).process_request(*args, **kwargs)


class ThreadedServer(RandomWaitMixin, SocketServer.ThreadingMixIn, WSGIServer):

    def __init__(self, server_address, RequestHandlerClass=None):
        BaseHTTPServer.HTTPServer.__init__(self, server_address,
                                            RequestHandlerClass)


class TestServerThread(threading.Thread):

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self._started = threading.Event()
        self._stopped = False
        self._error = None
        super(TestServerThread, self).__init__()

    def start(self):
        """ Start the server thread and wait for it to be ready """
        super(TestServerThread, self).start()
        self._started.wait()
        if self._error:
            raise self._error

    def stop(self):
        """ Stop the server """
        self._stopped = True
        # Send an http request to wake the server
        url = urllib.urlopen('http://%s:%d/login/' % (self.address, self.port))
        url.read()
        # Wait for server to finish
        self.join(5)
        if self._error:
            raise self._error

    def run(self):
        """Sets up test server and database and loops over
        handling http requests. """
        try:
            handler = basehttp.AdminMediaHandler(WSGIHandler())
            server_address = (self.address, self.port)
            httpd = httpd = ThreadedServer(server_address, WSGIRequestHandler)
            httpd.set_app(handler)
        except basehttp.WSGIServerException, e:
            self._error = e
            raise e
        finally:
            self._started.set()
       # Loop until we get a stop event.
        while not self._stopped:
            httpd.handle_request()
