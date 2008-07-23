"""Pylons middleware initialization"""
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool

from pylons import config
from pylons.error import error_template
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, \
    StaticJavascripts
from pylons.wsgiapp import PylonsApp

from cookieauth.cookieauth import CookieAuth
from twirlip.config.environment import load_environment

from signedheaders import HeaderSignatureCheckingMiddleware
from supervisorerrormiddleware import SupervisorErrorMiddleware
from wsseauth import WSSEAuthMiddleware

def make_app(global_conf, full_stack=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by
        another WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    # Configure the Pylons environment
    load_environment(global_conf, app_conf)

    # The Pylons WSGI app
    app = PylonsApp()

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)   

    # Establish the Registry for this application
    app = RegistryManager(app)

    if app_conf.get('openplans_wrapper') == 'TestingEnv':
        users = {'anon' : 'Anonymous',
                 'auth' : 'Authenticated',
                 'member' : 'ProjectMember',
                 'contentmanager' : 'ProjectContentManager',
                 'admin' : 'ProjectAdmin'
                 }
        from twirlip.lib.testing_env import TestingEnv        
        app = TestingEnv(app, users)
        app = CookieAuth(app, app_conf)
    elif app_conf.get('openplans_wrapper') == 'CookieAuth':
        app = HeaderSignatureCheckingMiddleware(app, app_conf)

    login_file = app_conf['cabochon_password_file']
    username, password = file(login_file).read().strip().split(":")

    if username:
        app = WSSEAuthMiddleware(app, {username : password}, required=False)    

    app = SupervisorErrorMiddleware(app)

    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, error_template=error_template,
                           **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)


    # Static files
    javascripts_app = StaticJavascripts()
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])

    return app
