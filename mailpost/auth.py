"""
Authenticate
A package that maps incoming email to HTTP requests
Mailpost version 0.0.1 alpha
(C) 2010 OTT Team
"""
import httplib, urllib, urllib2
import cookielib
from poster.streaminghttp import StreamingHTTPHandler,\
    StreamingHTTPRedirectHandler
    
if hasattr(httplib, "HTTPS"):
    from poster.streaminghttp import StreamingHTTPSHandler
        
def get_handlers():
    """
    get handlers registered by the poster.streaminghttp.register_openers, as
    we are overriding them by adding 2 new handlers
    """
    handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler]
    if hasattr(httplib, "HTTPS"):
        handlers.append(StreamingHTTPSHandler)

    return handlers

def authenticate(auth_data, request):
    """
    Format for auth_data:
    url: <url to login form> 
    form:
      username (name of the field in POST): value
      passwd (name of the field in POST): value
    """
    handlers = get_handlers()
    auth_url = auth_data.get('url', None)

    data = {}
    for key in auth_data['form']:
        data[key] = auth_data['form'][key]
   
    cj = cookielib.CookieJar()
    # build opener with HTTPCookieProcessor
    urlopener = urllib2.build_opener(urllib2.HTTPRedirectHandler,
                                     urllib2.HTTPCookieProcessor(cj),
                                     *handlers)
    
    urllib2.install_opener(urlopener)
    #setup cookie
    
    f = urllib2.urlopen(auth_url)
    f.close()        

    params = urllib.urlencode(data)
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    req = urllib2.Request(auth_url, params, txheaders)
    
    # perform login with params
    f = urllib2.urlopen(req)

    f.close()
    return cj, urlopener