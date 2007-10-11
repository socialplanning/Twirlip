def email(user, page):
    if not user.email:
        return
    send_mail (user.email, "The page %s has been updated" % page.name)


notification_methods = {'Email' : email}

def notify(method, user, page):
    notification_methods[method](user, page)

