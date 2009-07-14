messages = dict(
    update = dict(
        subject = 'Update notification - %(title)s - %(updater)s',
        body = """%(title)s has been updated by %(updater)s.  

Go to %(url)s to see it.

%(unsubscribe)s"""
        ),
    delete = dict(
        subject = 'Delete notification - %(title)s - %(updater)s',
        body = """%(title)s has been deleted by %(updater)s.

%(unsubscribe)s"""    
        ),
    create = dict(
        subject = '%(title)s has been created - %(updater)s',
        body = """%(title)s has been created by %(updater)s. 
 
Go to %(url)s to see it.

%(unsubscribe)s"""    
        ),
    unsubscribe = dict(
        subject = 'unsubscribe message',
        body = """To unsubscribe from these messages, visit
http://www.coactivate.org/people/%(user)s/account.
    """
        )
    )
