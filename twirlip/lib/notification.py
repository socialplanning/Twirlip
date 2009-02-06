from twirlip.lib.sendmail import send_mail
from twirlip.lib.messages import messages

import datetime 

def email(user, page, event_type, params):
    if not user.email:
        return

    message = messages[event_type]
    page_dict = page.sqlmeta.asDict()
    page_dict['updater'] = params['user']
    page_dict['unsubscribe'] = messages['unsubscribe']['body'] % dict(user = user.username)
    subject = message['subject'] % page_dict
    body = message['body'] % page_dict

    send_mail ('notification@openplans.org', user.email, subject, body)


notification_methods = {'Email' : email}

def notify(method, user, page, event_type, params):
    """Tell a user that an event to which they are subscribed
    has occurred.  Avoid notifying a user too often per page."""

    last_message = user.most_recent_message(page)
    if last_message and datetime.datetime.now() - last_message > datetime.timedelta(0, 300):
        return #too soon
    
    notification_methods[method](user, page, event_type, params)

