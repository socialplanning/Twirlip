"""Setup the Twirlip application"""
import logging

from paste.deploy import appconfig
from pylons import config

from twirlip.config.environment import load_environment
from twirlip.model import *
from twirlip.model.config import create_defaults

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup twirlip here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)

    if filename == "test.ini":
        for table in soClasses[::-1]:
            table.dropTable(ifExists=True)
    for table in soClasses:
        table.createTable(ifNotExists=True)

    create_defaults()
