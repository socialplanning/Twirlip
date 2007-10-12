from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on

class WatchController(BaseController):

    def control(self):
        url = request.environ['HTTP_X_TRANSCLUDED']
        try:
            page = Page.byUrl(url)
        except SQLObjectNotFound:
            return "" #no control
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
            preference = URLPreference.get(id)
        else:
            preference = URLPreference.lookup(c.user, request.params['url'])

        assert preference.user == c.user
        url = preference.url
        preference.destroySelf()
        return redirect_to(url)
        
        
