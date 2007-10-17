from twirlip.lib.sendmail import send_mail

def email(user, page):
    if not user.email:
        return

    message = "The page %s has been updated.  \nGo to %s to see it." % (page.title, page.url)
    subject = 'Update notification' 
    send_mail ('notification@openplans.org', user.email, subject, message)


notification_methods = {'Email' : email}

def notify(method, user, page, event_type=None):
    notification_methods[method](user, page)

