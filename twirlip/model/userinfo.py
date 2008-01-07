from pylons import config
import httplib2
from urllib import urlencode
import elementtree.ElementTree as ET

from logging import warn

def get_email(username):
    admin_file = config['topp_admin_info_filename']
    admin_info = tuple(file(admin_file).read().strip().split(":"))

    base_conf = config['base_conf']
    server = base_conf.get('applications', 'opencore uri')

    h = httplib2.Http()
    # because of some zope silliness we have to do this as a POST instead of basic auth
    data = {"__ac_name":admin_info[0], "__ac_password":admin_info[1]}
    body = urlencode(data)

    resp, content = h.request("%s/people/%s/info.xml" % (server, username), method="POST", body=body, redirections=0)
    
    if resp['status'] != '200':
        if resp['status'] == '302':
            # redirect probably means auth failed
            extra = '; did your admin authentication fail?'
        if resp['status'] == '400':
            # Probably Zope is gone
            extra = '; is Zope started?'
        else:
            extra = ''
        warn("Error retrieving user %s: status %s%s" 
            % (username, resp['status'], extra))
        return None #we've got to keep going
        #raise ValueError("Error retrieving user %s: status %s%s" 
        #                 % (username, resp['status'], extra))

    tree = ET.fromstring(content)
    return tree.findall('email')[0].text
