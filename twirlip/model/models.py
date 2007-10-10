#!/usr/bin/python

from sqlobject import *
from pylons.database import PackageHub
from sqlobject.dberrors import DuplicateEntryError
from twirlip.lib.notification import notify

hub = PackageHub("twirlip", pool_connections=False)
__connection__ = hub

from userinfo import get_email

class User(SQLObject):
    username = UnicodeCol(length=150, alternateID=True)
    email = UnicodeCol(length=150, default=None)
    event_preferences = MultipleJoin("EventPreference")
    url_preferences = MultipleJoin("URLPreference")
    auto_watch_preferences = MultipleJoin("AutoWatchPreference")    

    def _get_email(self):
        email = self._SO_get_email()
        if email:
            return email

        email = get_email(self.username)
        self.email = email
        return email

    def all_auto_watch_preferences(self):
        prefs = dict((x.auto_watch_classID, x) for x in self.auto_watch_preferences)
        out = []
        for awc in AutoWatchClass.select():
            if awc.id in prefs:
                out.append((awc, True))
            else:
                out.append((awc, False))

        return out
                
    @classmethod
    def get_or_create(cls, username):
        try:
            return cls.byUsername(username)
        except SQLObjectNotFound:
            try:
                user = cls(username=username)
                user.init_preferences()
                return user
            except DuplicateEntryError:
                return cls.byUsername(username)


    def init_preferences(self, force=False):
        if not force and len(self.event_preferences):
            return #already have some prefs
        
        for event_class in EventClass.select():
            try:
                EventPreference(user=self, event_class=event_class, notification_method=NotificationMethod.NONE)
            except DuplicateEntryError:
                pass #we already have this preference

        for awc in AutoWatchClass.selectBy(default_on=True):
            try:
                AutoWatchPreference(user=self, auto_watch_class = awc)
            except DuplicateEntryError:
                pass #we already have this preference
            
class SecurityContext(SQLObject):
    """This represents a set of objects which share security permissions.  For
    example, all tasks on a task list share the same security."""
    url = StringCol(length=512)

    @classmethod
    def byUrl(cls, url):
        try:
            return cls.selectBy(url=url)[0]
        except IndexError:
            return cls(url=url)

    url_index = DatabaseIndex('url', unique=True)
    
class Page(SQLObject):
    """This represents a URL that can be watched."""
    url = StringCol(length=512, alternateID=True)
    name = StringCol() #usually something like ${Project}: ${page_or_task_name}
    securityContext = ForeignKey("SecurityContext")

    def notify(self):
        for pref in URLPreference.selectBy(page=self):
            user = pref.user
            notify(pref.notification_method.name, user, self)

class PageClass(SQLObject):
    """A category of page, like task, wiki page, or project
    (encompassing all notifications within the project as well as
    stats notes).  Pages can belong to multiple categories."""
    name = StringCol(length=20, alternateID=True)
    event_classes = RelatedJoin('EventClass')
    
class Association(SQLObject):
    """This handles containment and other similar relationships.  When
    updates on one object will trigger notification on another, then
    the first object is said to be the child of the first."""
    parent = ForeignKey("Page")
    child = ForeignKey("Page")
    everything_index = DatabaseIndex('parent', 'child', unique=True)
    
class EventClass(SQLObject):
    """This represents a type of event.  Some event types will only
    apply to certain page classes."""
    name = StringCol(length=20, alternateID=True)
    display_name = StringCol()
    page_classes = RelatedJoin('PageClass')
    
class NotificationMethod(SQLObject):
    """None, Email, account page, SMS, carrier pigeon..."""
    name = StringCol(length=20, alternateID=True)

NotificationMethod.NONE = NotificationMethod.byName("None")

class AutoWatchClass(SQLObject):
    name = StringCol(length=20, alternateID=True)
    display_name = StringCol()
    default_on = BoolCol(default=False)
    preferences = SQLMultipleJoin('AutoWatchPreference')
    
class EventPreference(SQLObject):
    user = ForeignKey("User")
    event_class = ForeignKey("EventClass")
    notification_method = ForeignKey("NotificationMethod")
    everything_index = DatabaseIndex('user',
                                     'event_class',
                                     'notification_method', unique=True)

    @classmethod
    def byUserAndEventClassName(cls, user, event_class_name):
        return cls.select(
            (EventPreference.q.userID == user.id) &
            (EventPreference.q.event_classID == EventClass.q.id) &
            (EventClass.q.name == event_class_name))

class URLPreference(SQLObject):
    user = ForeignKey("User")
    page = ForeignKey("Page")
    notification_method = ForeignKey("NotificationMethod")
    everything_index = DatabaseIndex('user', 'page', unique=True)
    everything_index_by_page = DatabaseIndex('page', 'user', unique=True)        

    @classmethod
    def lookup(cls, user, url):
        results = cls.select((cls.q.userID == user.id) &
                             (cls.q.pageID == Page.q.id) &
                             (Page.q.url == url))
        try:
            return results[0]
        except IndexError:
            return None

    @classmethod
    def create(cls, user, url=None, page=None):
        if page:
            assert url is None or page.url == url
        else:
            try:
                page = Page.byUrl(url)
            except SQLObjectNotFound:
                print "Can't watch an object that we haven't heard of yet"
                return

        try:        
            return cls(user=user, page=page, notification_method = NotificationMethod.byName('Email')) #fixme: make method configurable
        except DuplicateEntryError:
            #you're already there
            return cls.lookup(user, url)
                
class AutoWatchPreference(SQLObject):
    user = ForeignKey("User")
    auto_watch_class = ForeignKey("AutoWatchClass")
    everything_index = DatabaseIndex('user', 'auto_watch_class', unique=True)    


soClasses = [
    Association,
    AutoWatchClass,
    AutoWatchPreference,
    EventClass,
    EventPreference,
    NotificationMethod,
    Page,
    PageClass,
    SecurityContext,
    URLPreference,
    User
]
