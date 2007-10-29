messages = dict(
    update = dict(
    subject = 'Update notification - %(title)s',
    body = """The page %(title)s has been updated.  \nGo to %(url)s to see it.
%(unsubscribe)s"""
    ),
    delete = dict(
    subject = 'Delete notification - %(title)s',
    body = """The page %(title)s has been deleted.
%(unsubscribe)s"""    
    ),
    create = dict(
    subject = 'Page created - %(title)s',
    body = """The page %(title)s has been deleted.
%(unsubscribe)s"""    
    ),
    unsubscribe = dict(
    subject = 'unsubscribe message',
    body = """To unsubscribe from these messages, visit
http://www.openplans.org/people/%(user)s/account.
    """
    )
)
