from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on

class UserController(BaseController):

    @dispatch_on(POST="do_watchlist")
    def watchlist(self):
        c.done_url = request.environ.get('HTTP_X_TRANSCLUDED', h.url_for())
        c.watches = c.user.url_preferences
        return render("/watchlist.mako")

    def do_watchlist(self):
        for id in request.params.getall('check:list'):
            preference = URLPreference.get(id)
            assert preference.user == c.user
            preference.destroySelf()
        return redirect_to(str(request.params['done_url']))

    @dispatch_on(POST="do_preferences")
    def preferences(self):
        c.done_url = request.environ.get('HTTP_X_TRANSCLUDED', h.url_for())
        return render("/preferences.mako")

    def do_preferences(self):
        for awc in AutoWatchClass.select():
            if request.params.get("awc_%s" % awc.name):
                try:
                    AutoWatchPreference(user=c.user, auto_watch_class=awc)
                except DuplicateEntryError:
                    pass #already have that one
            else:
                try:
                    AutoWatchPreference.selectBy(user=c.user, auto_watch_class=awc)[0].destroySelf()
                except IndexError:
                    pass

        return redirect_to(str(request.params['done_url']))
