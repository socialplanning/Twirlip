from twirlip.lib.sendmail import send_mail
from twirlip.lib.messages import messages

def email(user, page, event_type):
    if not user.email:
        return

    message = messages['event_type']
    page_dict = page.sqlmeta.asDict()
    subject = message['subject'] % page_dict
    body = message['body'] % page_dict

    send_mail ('notification@openplans.org', user.email, subject, message)


notification_methods = {'Email' : email}

def notify(method, user, page, event_type):
    notification_methods[method](user, page, event_type)

