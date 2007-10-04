"""Setup the Twirlip application"""
import logging

from paste.deploy import appconfig
from pylons import config

from twirlip.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)

    from twirlip.model import soClasses
    from twirlip.model.config import create_defaults

    if filename == "test.ini":
        for table in soClasses[::-1]:
            table.dropTable(ifExists=True)
    for table in soClasses:
        table.createTable(ifNotExists=True)

    create_defaults()
