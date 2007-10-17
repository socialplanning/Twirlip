from twirlip.tests import *
from twirlip.model import *

class TestUserController(TestController):

    def test_config(self):
        print "Cabochon must be running!"
        app = self.get_app('admin')
        response = app.get(url_for(controller='config', action='index'))
        response.mustcontain('configured')
        
        response = app.get(url_for(controller='user', action='preferences'))
        response.mustcontain('Subscribe me to events automatically when:')
        response.mustcontain('a task is assigned to me')

        #a task is assigned to me
        form = response.forms[0]
        form['awc_task_assigned'] = 'No'
        response = form.submit().follow()
        
        response.mustcontain('<option value="No" selected')

        admin = User.byUsername('admin')
        awc = AutoWatchClass.byName('task_assigned')
        assert AutoWatchPreference.selectBy(user='admin', auto_watch_class = awc).count() == 0
        
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

