from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on
from pylons.decorators import jsonify
from simplejson import loads

class PageController(BaseController):
    @dispatch_on(POST='do_create')
    def index(self):
        pass

    @jsonify
    def do_create(self):
        context = SecurityContext.byUrl(self.params['context'])
        try:
            Page(url=self.params['url'], 
                 name=self.params['name'],
                 securityContext=context)
        except DuplicateEntryError:
            page = Page.selectBy(url=self.params['url'])[0]
            page.set(name = self.params['name'], securityContext = context)
            
        return {'status' : 'accepted'}

    @jsonify
    def edit(self):
        context = SecurityContext.byUrl(self.params['context'])
        try:
            page = Page.selectBy(url=self.params['url'])[0]
            page.set(name = self.params['name'], securityContext = context)            
        except IndexError:
            page = Page(url=self.params['url'], 
                        name=self.params['name'],
                        securityContext=context)


        #create any necessary users
        for username in self.params.get('relevant_users', []):
            User.get_or_create(username)
        
        #set up autowatches
        for cls in self.params['event_class']:
            cls, value = cls
            user = User.get_or_create(value)
            try:
                awc = AutoWatchClass.byName(cls)
            except SQLObjectNotFound:
                continue
            try:
                pref = AutoWatchPreference.selectBy(auto_watch_class=awc, user=user)[0]
                print "exists pref", pref
            except IndexError:
                pass
            URLPreference.create(user, page=page)
        page.notify()
        
        return {'status' : 'accepted'}

    @jsonify
    def email_changed(self):
        
        User.get_or_create(self.params['user']).email=self.params['email']

        return {'status' : 'accepted'}        
