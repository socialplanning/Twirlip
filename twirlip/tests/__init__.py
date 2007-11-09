"""Pylons application test package

When the test runner finds and executes tests within this directory,
this file will be loaded to setup the test environment.

It registers the root directory of the project in sys.path and
pkg_resources, in case the project hasn't been installed with
setuptools. It also initializes the application via websetup (paster
setup-app) with the project's test.ini configuration file.
"""
import os
import sys
from unittest import TestCase

import pkg_resources
import paste.fixture
import paste.script.appinstall
from paste.deploy import loadapp
from routes import url_for

from wsseauth import wsse_header
from simplejson import dumps
import time
from wsgi_intercept import add_wsgi_intercept, httplib2_intercept
from server import TwirlipServerFixture

__all__ = ['url_for', 'TestController']

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(os.path.dirname(here_dir))

sys.path.insert(0, conf_dir)
pkg_resources.working_set.add_entry(conf_dir)
pkg_resources.require('Paste')
pkg_resources.require('PasteScript')

test_file = os.path.join(conf_dir, 'test.ini')
cmd = paste.script.appinstall.SetupCommand('setup-app')
cmd.run([test_file])

def mock_email(user, page, event_class):
    from pylons import request
    request.environ['paste.testing_variables']['email'] = dict(user=user, event_class=event_class)

class TestController(TestCase):

    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = wsgiapp
        from twirlip.lib.notification import notification_methods
        notification_methods['Email'] = mock_email

        httplib2_intercept.install()
        add_wsgi_intercept('testserver.example.com', 80, TwirlipServerFixture)
        TestCase.__init__(self, *args, **kwargs)
        
    def get_app(self, username):
        encoded = 'Basic ' + (username + ':nopassword').encode('base64')
        return paste.fixture.TestApp(self.app, extra_environ={'HTTP_AUTHORIZATION': encoded})

    def cabochon_message(self, path, params):
        #we need a wsse header

        params = dict((key, dumps(value)) for key, value in params.items())
        extra_environ = {'HTTP_AUTHORIZATION' : 'WSSE profile="UsernameToken"',
                         'HTTP_X_WSSE' : wsse_header('topp', 'secret')
                         }
        app = paste.fixture.TestApp(self.app, extra_environ=extra_environ)
        response = app.post(path, params = params)
        assert response.body == '{"status": "accepted"}'
        return response
