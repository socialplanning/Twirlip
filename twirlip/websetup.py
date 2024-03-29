"""Setup the Twirlip application"""
import logging

from paste.deploy import appconfig
from pylons import config

from twirlip.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    conf = appconfig('config:' + filename + '#' + section.split(':')[1])
    load_environment(conf.global_conf, conf.local_conf)

    from twirlip.model import soClasses, hub
    from twirlip.model.config import create_defaults

    if filename.endswith("test.ini"):
        for table in soClasses[::-1]:
            table.dropTable(ifExists=True)

    constraints = []
    for table in soClasses:
        _constraints = table.createTable(ifNotExists=True, applyConstraints=False)
        if _constraints is not None:
            constraints += _constraints

    connection = hub.hub.getConnection()
    for constraint in constraints:
        connection.query(constraint)

    create_defaults()

    print """Now start the application and visit /config to hook
    Twirlip up to Cabochon"""
