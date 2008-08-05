from twirlip.model.models import *
from sqlobject.dberrors import DuplicateEntryError

def create_defaults():
    notification_methods = ["None", "Email"] #and more ...

    page_classes = ["task", "wiki page"] #and more...

    event_classes = [
        ('assign', 'A %s is assigned'),
        ('comment', 'Someone comments on a %s'),
        ('delete', 'A %s is deleted'),
        ('attribute', "A %s's description or other data has changed"),
    # and more    
        ]


    event_class_page_classes = dict(
        Task = ['assign', 'comment', 'delete', 'attribute']
        )

    auto_watch_classes = [('task_assigned', 'a task is assigned to me'),
                          ('page_edited', 'I create or edit a wiki page')]

    for method in notification_methods:
        try:
            NotificationMethod(name=method)
        except DuplicateEntryError:
            pass

    for name in page_classes:
        try:
            PageClass(name=name)
        except DuplicateEntryError:
            pass

    for name, display in event_classes:
        try:
            EventClass(name=name, display_name=display)
        except DuplicateEntryError:
            pass
        
    for pc, ecs in event_class_page_classes.items():
        pc = PageClass.byName(pc)
        pc_event_classes = set(pc.event_classes)
        for ec in ecs:
            try:
                ec = EventClass.byName(ec)
                if not ec in pc_event_classes:
                    pc.addEventClass(ec)
            except DuplicateEntryError:
                pass

    for name, display in auto_watch_classes:
        try:
            AutoWatchClass(name=name, display_name=display, default_on=True)
        except DuplicateEntryError:
            pass
