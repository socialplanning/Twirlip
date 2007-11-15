"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

from paste.wsgiwrappers import WSGIResponse

import twirlip.lib.helpers as h
from twirlip.model import *

from simplejson import loads

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        controller = environ['pylons.routes_dict']['controller']

        if controller == 'template':
            return WSGIController.__call__(self, environ, start_response)
        username = environ.get('REMOTE_USER')
        if not username and controller != 'config':
            return WSGIResponse(content='please log in', code=401)

        if environ.get('AUTHENTICATION_METHOD') != 'WSSE':
            if controller == 'watch' or controller == 'user':
                c.user = User.get_or_create(username)
            else:
                if (environ.get('REMOTE_ADDR').startswith('127.0.0.1') and controller == 'config') or controller == 'error':
                    #local users can configure Twirlip and see errors
                    pass
                else:
                    #all other authentication must be by wsse
                    return WSGIResponse(code=403, content='You need to authenticate with wsse to access %s ' % controller)
            
        if controller == 'page':
            #json
            self.params = {}
            for param, value in request.params.items():
                self.params[param] = loads(value)
                    
        return WSGIController.__call__(self, environ, start_response)

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
