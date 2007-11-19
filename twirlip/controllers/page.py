from twirlip.lib.base import *
from pylons.decorators.rest import dispatch_on
from pylons.decorators import jsonify
from simplejson import loads
import re
class PageController(BaseController):
    canonicalize_url_re = re.compile('(http://[^/]+):80')
    
    @dispatch_on(POST='do_create')
    def index(self):
        pass

    @dispatch_on(POST='do_create')
    def create(self):
        pass


    @jsonify
    def do_create(self):
        """Called from cabochon when a page is created."""
        context = SecurityContext.byUrl(self.params['context'])
        url = self.params['url']
        url = self.canonicalize_url_re.sub('\\1', url)

        try:
            page = Page(url=url, 
                        title=self.params['title'],
                        securityContext=context)
        except DuplicateEntryError:
            page = Page.selectBy(url=url)[0]
            page.set(title = self.params['title'], securityContext = context)

        self._set_up_autowatches(page)

        page.notify('create')
        
        return {'status' : 'accepted'}

    @jsonify
    def edit(self):
        """Called from cabochon when a page is edited."""        
        context = SecurityContext.byUrl(self.params['context'])
        try:
            page = Page.selectBy(url=self.params['url'])[0]
            page.set(title = self.params['title'], securityContext = context)            
        except IndexError:
            page = Page(url=self.params['url'], 
                        title=self.params['title'],
                        securityContext=context)


        #create any necessary users
        for username in self.params.get('relevant_users', []):
            if username:
                User.get_or_create(username)

        self._set_up_autowatches(page)
        page.notify('update')
        
        return {'status' : 'accepted'}

    def _set_up_autowatches(self, page):
        for cls in self.params.get('event_class', []):
            cls, value = cls
            if not value:
                continue
            user = User.get_or_create(value)
            try:
                awc = AutoWatchClass.byName(cls)
            except SQLObjectNotFound:
                continue
            try:
                pref = AutoWatchPreference.selectBy(auto_watch_class=awc, user=user)[0]
                #if pref exists:
                URLPreference.create(user, page=page)
            except IndexError:
                pass

    @jsonify
    def delete(self):
        """Called from cabochon when a page is deleted."""                
        try:
            page = Page.selectBy(url=self.params['url'])[0]
            page.notify('delete')            
            page.destroySelf()
        except IndexError:
            pass
        return {'status' : 'accepted'}        

    @jsonify
    def email_changed(self):
        """Called from cabochon when a user's email address changes."""
        User.get_or_create(self.params['user']).email=self.params['email']

        return {'status' : 'accepted'}        
