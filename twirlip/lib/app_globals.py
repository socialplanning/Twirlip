"""The application's Globals object"""
from pylons import config

from ConfigParser import ConfigParser

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        base_conf = ConfigParser()
        base_conf.read(config['base_config'])
        config['base_conf'] = base_conf
