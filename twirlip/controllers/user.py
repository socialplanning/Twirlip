from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on

class UserController(BaseController):

    @dispatch_on(POST="do_preferences")
    def preferences(self):
        c.user.init_preferences() #if they aren't already set up
        return render("/preferences.mako")

    def do_preferences(self):
        for param, value in request.params.items():
            if not "_" in param:
                continue
            cls, name = param.split("_", 1)
            if cls == "awc":
                awc = AutoWatchClass.byName(name)
                if value == "Yes":
                    try:
                        AutoWatchPreference(user=c.user, auto_watch_class=awc)
                    except DuplicateEntryError:
                        pass #already have that one
                else:
                    try:
                        AutoWatchPreference.selectBy(user=c.user, auto_watch_class=awc)[0].destroySelf()
                    except IndexError:
                        pass

            
            elif cls == "ec":
                ec = EventPreference.byUserAndEventClassName(c.user, name)
                ec.notification_method = NotificationMethod.byName(value)

            
        return redirect_to(action="preferences")
