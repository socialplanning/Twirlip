# Copyright (C) 2007 The Open Planning Project

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301
# USA

from twirlip.lib.base import *
from twirlip.model import *
from cabochonserver import ServerInstaller
from pylons import config

class ConfigController(BaseController):
    def index(self):
        event_server = config['base_conf'].get('applications', 'cabochon uri')

        login_file = config['cabochon_password_file']
        username, password = file(login_file).read().strip().split(":")
        
        installer = ServerInstaller(".servers", username, password)
        
        installer.addEvent(event_server, 'create_page', h.url_for(controller='page', action='create', qualified=True))
        installer.addEvent(event_server, 'edit_page', h.url_for(controller='page', action='edit', qualified=True))
        installer.addEvent(event_server, 'delete_page', h.url_for(controller='page', action='delete', qualified=True))        
        installer.addEvent(event_server, 'email_changed', h.url_for(controller='page', action='email_changed', qualified=True))



        installer.save()
        return "OK, you're configured.  Go have fun."
