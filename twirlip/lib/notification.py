from twirlip.lib.sendmail import send_mail

def email(user, page):
    if not user.email:
        return
    send_mail ('notification@openplans.org', user.email, 'Update notification', "The page %s has been updated" % page.name)


notification_methods = {'Email' : email}

def notify(method, user, page):
    notification_methods[method](user, page)

