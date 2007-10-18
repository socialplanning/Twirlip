# This server will do security context authentication.

from threading import Thread
from wsgiutils import wsgiServer
import paste
import time
import re


class TwirlipTestServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self._server_fixture = None
        
    @property
    def server_fixture(self):
        while not self._server_fixture:
            time.sleep(0)
        return self._server_fixture

    def run(self):
        self._server_fixture = TwirlipServerFixture()
        server = wsgiServer.WSGIServer (('localhost', 10424), {'/': self.server_fixture}, serveFiles = False)
        server.serve_forever()       

        
class TwirlipServerFixture:
    wsse_username_re = re.compile('Username="(\w+)"')
    def __init__(self):
        self.requests_received = []

    def clear(self):
        self.requests_received = []

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        req = paste.wsgiwrappers.WSGIRequest(environ)

        req_dict = {'path' :  environ['PATH_INFO'], 'method' : environ['REQUEST_METHOD'], 'params' : req.params}

        if environ.get('HTTP_X_WSSE'):
            match = self.wsse_username_re.search(environ.get('HTTP_X_WSSE'))
            req_dict['username'] = match.group(1) #assume user logged in correctly
        self.requests_received.append(req_dict)
        
        if path_info.startswith('/openplans'):
            #handle userinfo requests here
            path = path_info[len("/openplans/people/"):]
            username, infoxml = path.split("/")
            assert infoxml == "info.xml"
            status = '200 OK'
            start_response(status, [('Content-type', 'text/plain')])
            return ['<info><name>%s</name><email>%s@example.com</email></info>' % (username, username)]
        elif path_info == '/forbidden':
            status = '403 access denied'
            start_response(status, [('Content-type', 'text/plain')])
            return ['you lose']
        elif path_info == '/accepted':
            status = '200 OK'
            start_response(status, [('Location', '/redirected')])
            return ['ftw!']
        else:
            status = '200 OK'
            start_response(status, [('Content-type', 'text/plain')])
            return ['{"status" : "accepted"}']

        
