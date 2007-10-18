from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on

from twirlip.lib.helpers import oc_json_response

class WatchController(BaseController):

    def control(self):
        url = request.environ['HTTP_X_TRANSCLUDED']
        try:
            page = Page.byUrl(url)
        except SQLObjectNotFound:
            return "" #no control
        if not page.securityContext.can_read(c.user):
            return ""
        
        pref = URLPreference.lookup(c.user, url)
        c.is_watching = bool(pref)
        c.url = url
        return render("/control.mako")

    
    def watch(self):
        url = str(request.params['url'])
        URLPreference.create(c.user, url=url)
        return redirect_to(url)
        
    def unwatch(self, id=None):
        if id:
            try:
                preference = URLPreference.get(id)
            except SQLObjectNotFound:
                preference = None
        else:
            preference = URLPreference.lookup(c.user, request.params['url'])

        if not preference:
            if request.params.get('ajax'):
                #from prefs page
                return oc_json_response({"up_%s" % id: {'action': 'delete'}})
            else:
                return redirect_to(request.params['url'].encode("utf-8"))
            
        assert preference.user == c.user
        url = preference.page.url
        preference.destroySelf()
        if id:
            return oc_json_response({"up_%s" % id: {'action': 'delete'}})
        else:
            return redirect_to(url)
        
        
