from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on

class WatchController(BaseController):

    def control(self):
        url = request.environ['HTTP_X_TRANSCLUDED']
        pref = URLPreference.lookup(c.user, url)
        c.is_watching = bool(pref)
        c.url = url
        return render("/control.mako")

    
    def watch(self):
        url = str(request.params['url'])
        URLPreference.create(c.user, url)
        return redirect_to(url)
        
        
