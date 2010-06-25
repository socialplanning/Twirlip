from email.Message import Message
import smtplib
from pylons import config
import re
from warnings import warn

class EmailMessage:
    subjectline_re = re.compile("^Subject: [^\n]+$(.*)", re.S|re.M)
    varsub_re = re.compile("${(\w+)}")
        
    def __init__(self, message_name, **kw):
        import nz.lib.emailmessages as messages
        raw_message = getattr(messages, message_name)
        match = subjectline.re.match(raw_message)
        if match:
            self.subject = match.group(1)
            raw_message = match.group(2)
        else:
            self.subject = ''

        self.body = varsub_re.sub(lambda var: kw[var], raw_message)
        
    def send(self, sender, to):
        send_mail(sender, to, self.subject, self.body)

def send_mail(sender, to, subject, body):
    glob_email = config.get('global_email_override')
    if glob_email:
        to = glob_email
    message = Message()
    message["To"] = to
    message["From"] = sender
    message["Subject"] = subject
    message.set_payload(body.encode('utf-8'))
    server = open_server()
    try:
        server.sendmail(sender, to, message.as_string())
        warn("mail sent successfully to %s" % to)
    except smtplib.SMTPRecipientsRefused, e:
        from pprint import pformat
        warn("%r: unable to send mail to %s" % (pformat(e.recipients), to)) 
    server.quit()

def open_server():
    smtp_server = config.get('smtp_server', 'localhost')
    smtp_username = config.get('smtp_username')
    server = smtplib.SMTP(smtp_server)
    if smtp_username:
        smtp_password_file = config.get('smtp_password_file')
        if not smtp_password_file:
            raise Exception(
                "smtp_username is set, but not smtp_password_file")
        f = open(smtp_password_file)
        password = f.read().strip()
        f.close()
        server.login(smtp_username, password)
    return server

        
