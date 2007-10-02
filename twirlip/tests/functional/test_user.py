from twirlip.tests import *

class TestUserController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='userx', action='preferences'))
        # Test response...
