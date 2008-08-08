from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on
from pylons.decorators.secure import authenticate_form

from twirlip.lib.helpers import oc_json_response

from urllib import quote

class WatchController(BaseController):

    def control(self):
        try:       
            url = request.environ['HTTP_X_TRANSCLUDED']
        except KeyError:
            url = request.params['url']

        #we're going to trust that the user can view this page, since this is just to display
        #the control.
        #try:
        #    page = Page.byUrl(url)
        #except SQLObjectNotFound:
        #    return "<html><head></head><body><div><!-- twirlip: no such page --></div></body></html>" #no control

        #if not page.securityContext.can_read(c.user):
        #    return "<html><head></head><body><div><!-- twirlip: can't access page --></div></body></html>"
        
        pref = URLPreference.lookup(c.user, url)
        c.is_watching = bool(pref)
        c.url = url
        return render("/control.mako")

    @authenticate_form
    def watch(self):
        """Watch one or more pages.  Two modes:

        - From control, returns ajax to replace the 'watch' with the
        'unwatch' control.
        - From account page, return ajax to add rows for tasks'
        """
        #fixme: handle multiple urls
        urls = str(request.params['url']).split("\x00")
        preferences = []
        for url in urls:
            preferences.append(URLPreference.create(c.user, url=url))
            c.url = url
        
        if request.params.get('undo'):
            return oc_json_response(
                {"watch_table": {'action': 'append',
                                 'html' : "".join(render("/_url_preference_row.mako", preference=preference) for preference in preferences)}}

                )
        else:
            c.is_watching = True
            
            return oc_json_response(
                {"twirlip_control": {'action': 'replace',
                                     'html' : render("/_control.mako")}})


    @authenticate_form
    def unwatch(self, id=None):       
        """Stop watching one or more pages.  Supports three modes of operation:
        bulk (returns ajax to remove rows),
        account page-ajax (returns ajax to replace for a row)
        control (returns ajax to replace the control)
        """

        def undo_psm(urls):
            container = """
<div id="oc-statusMessage-container">
    <div class="oc-statusMessage oc-js-closeable">
       You have just stopped watching some pages.  <a href="%s" class="oc-actionLink oc-js-actionPost">Undo this.</a>
    </div>
</div>"""
            undo_url = h.secure_url_for(action='watch', url=urls, undo=1)
            return dict(
                action = 'replace',
                html = container % undo_url
                )

        #from the user's account page, bulk update
        if request.params.get('task|watchlist'):
            commands = {}
            undo_list = []
            for id in request.params.getall('check:list'):
                try:
                    preference = URLPreference.get(id)
                    url = preference.page.url
                    if preference.user != c.user:
                        continue
                    preference.destroySelf()
                    commands["up_%s" % id] =  {'action': 'delete'}
                    undo_list.append(url)
                except SQLObjectNotFound:
                    continue

            num_watches = URLPreference.selectBy(user=c.user).count()
            commands['num_watches'] = dict(action = "replace",
                                           html = '<span id="num_watches">%d</span>' % num_watches)
            commands['oc-statusMessage-container'] = undo_psm("\0".join(undo_list))
            return oc_json_response(commands)
            

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

        
        
