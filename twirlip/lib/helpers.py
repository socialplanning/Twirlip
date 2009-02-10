"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from twirlip.model import *
from simplejson import dumps
from paste.wsgiwrappers import WSGIResponse
from webhelpers.rails import secure_form_tag, secure_form, link_to
from pylons.controllers.util import url_for

def notification_dropdown(name, selected=None):
    options = [n.name for n in NotificationMethod.select()]
    options = options_for_select(options, selected)
    return select(name, options)

def yes_no_dropdown(name, yes=True):
    options = options_for_select(["Yes", "No"], yes and "Yes" or "No")
    return select(name, options)

def escape(value):
    value = value.replace("&", "&amp;")    
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    return value

def oc_json_response(obj, status=''):
    
    #x-deliverance-no-theme
    if not 'oc-statusMessage-container' in obj:
        if status:
            obj['oc-statusMessage-container'] = {'action': 'replace', 'html': '\n <div id="oc-statusMessage-container"><div class="oc-statusMessage oc-js-closeable">%s</div></div>\n\n' % status, 'effects': 'blink'}
            
        else:
            obj['oc-statusMessage-container'] = {'action': 'replace', 'html': '\n <div id="oc-statusMessage-container"> </div>\n\n', 'effects': 'blink'}

    response = WSGIResponse()
    response.write("<html><body>%s</body></html>" % escape(dumps(obj)))
    response.headers['X-Deliverance-No-Theme'] = '1'
    return response
#    return "<html><body>%s</body></html>" % escape(dumps(obj))

def secure_url_for(**kw):
    kw[secure_form_tag.token_key] = secure_form_tag.authentication_token()
    return url_for(**kw)

def hidden_authenticator():
   return '<input name="%s" value="%s" type="hidden"/>' % (secure_form_tag.token_key, secure_form_tag.authentication_token())
