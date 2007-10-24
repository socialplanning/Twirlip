from twirlip.tests import *
from twirlip.model import *

class TestUserController(TestController):

    def test_config(self):
        app = self.get_app('admin')
        response = app.get(url_for(controller='config', action='index'))
        response.mustcontain('configured')
        
        response = app.get(url_for(controller='user', action='preferences'))
        response.mustcontain('a task is assigned to me')

        #a task is assigned to me
        form = response.forms[0]
        form['awc_task_assigned'].checked = False
        response = form.submit().follow()
        
        assert 'checked' not in response.body

        admin = User.byUsername('admin')
        awc = AutoWatchClass.byName('task_assigned')
        assert AutoWatchPreference.selectBy(user=admin, auto_watch_class = awc).count() == 0
        
        #now let's have a task assigned
        self.cabochon_message('/page/edit', params=dict
                              (url = 'http://morx.example.com/fleem',
                               title = 'page morx fleem title',
                               context = 'http://localhost:10424/accepted',
                               event_class = [('task_assigned', 'admin')],
                               ))
        
        #check that the user is not subscribed.
        admin = User.byUsername('admin')
        page = Page.byUrl('http://morx.example.com/fleem')
        assert page.title == 'page morx fleem title'
        prefs = URLPreference.selectBy(user=admin, page=page)
        assert prefs.count() == 0


    def test_auto_watch(self):
        app = self.get_app('someuser')
        
        #assign a task to the user
        res = self.cabochon_message(
            '/page/edit', params=dict
            (url = 'http://morx.example.com/fleem',
             title = 'page morx fleem title',
             context = 'http://localhost:10424/accepted',
             event_class = [('task_assigned', 'someuser')],
             ))
        
        #check that the user is now subscribed.
        someuser = User.byUsername('someuser')
        page = Page.byUrl('http://morx.example.com/fleem')
        assert page.title == 'page morx fleem title'
        prefs = URLPreference.selectBy(user=someuser, page=page)
        assert prefs.count() == 1

        #check that the user is notified
        assert res.email['address'] == 'someuser@example.com'
        assert res.email['event_class'] == 'update'

        #and that the sub appears on the watchlist
        res = app.get(url_for(controller='user', action='watchlist'), extra_environ=dict(HTTP_X_TRANSCLUDED='http://somewhere'))
        res.mustcontain('page morx fleem title')

        #and that we can unsub
        #using checkboxes
        
        form = res.forms[0]
        form['check:list'].checked = True
        res = form.submit()
        assert res.header_dict['location'] == 'http://somewhere'
        res = app.get(url_for(controller='user', action='watchlist'))
        assert not 'page morx fleem title' in res
        
    #check security context
    def test_security(self):
        app = self.get_app('morx')
        #create a page with a security context which does not allow morx to view
        self.cabochon_message(
            '/page/create', params=dict
            (url = 'http://morx.example.com/nogo',
             title = 'page morx fleem title',
             context = 'http://localhost:10424/forbidden',
             ))

        #check that the control is empty
        res = app.get(url_for(controller='watch', action='control'), extra_environ=dict(HTTP_X_TRANSCLUDED='http://morx.example.com/nogo'))
        assert res.body == '<html><head></head><body></body></html>'
        
        #try to watch
        res = app.get(url_for(controller='watch', action='watch', url='http://morx.example.com/nogo'))

        #but it fails
        user = User.byUsername('morx')
        page = Page.byUrl('http://morx.example.com/nogo')
        prefs = URLPreference.selectBy(user=user, page=page)
        assert prefs.count() == 0
