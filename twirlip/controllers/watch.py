from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on
from pylons.decorators.secure import authenticate_form

from twirlip.lib.helpers import oc_json_response

class WatchController(BaseController):

    def control(self):
        try:       
            url = request.environ['HTTP_X_TRANSCLUDED']
        except KeyError:
            url = request.params['url']

        try:
            page = Page.byUrl(url)
        except SQLObjectNotFound:
            return "<html><head></head><body><div></div></body></html>" #no control

        if not page.securityContext.can_read(c.user):
            return "<html><head></head><body></body></html>"
        
        pref = URLPreference.lookup(c.user, url)
        c.is_watching = bool(pref)
        c.url = url
        return render("/control.mako")

    @authenticate_form
    def watch(self):
        url = str(request.params['url'])
        URLPreference.create(c.user, url=url)
        c.is_watching = True
        c.url = url
        return oc_json_response(
            {"twirlip_control": {'action': 'replace', 'html' : render("/_control.mako")}})


    @authenticate_form
    def unwatch(self, id=None):       
        """Stop watching one or more pages.  Supports three modes of operation:
        bulk (redirects back to a given URL),
        account page-ajax (returns ajax to replace for a row)
        control (returns ajax to replace the control)
        """
        #from the user's account page, bulk update
        if request.params.get('task|watchlist'):
            for id in request.params.getall('check:list'):
                try:
                    preference = URLPreference.get(id)
                    if preference.user != c.user:
                        continue
                    preference.destroySelf()
                except SQLObjectNotFound:
                    continue
            return redirect_to(str(request.params.get('done_url')))

        #from user's account page, ajax
        if id:
            try:
                preference = URLPreference.get(id)
                assert preference.user == c.user
                preference.destroySelf()
            except SQLObjectNotFound:
                pass
                
            num_watches = URLPreference.selectBy(user=c.user).count()
            return oc_json_response(
                {"up_%s" % id: {'action': 'delete'},
                 'num_watches' :
                 dict(action = "replace",
                      html = '<span id="num_watches">%d</span>' % num_watches)
                })
            
        else:
            #from control, ajax
            url = request.params['url']
            preference = URLPreference.lookup(c.user, url)
            if preference:
                assert preference.user == c.user
                preference.destroySelf()
                
            c.is_watching = False
            c.url = url
            return oc_json_response(
                {"twirlip_control":
                 {'action': 'replace',
                  'html' : render("/_control.mako")}})            

        
        
