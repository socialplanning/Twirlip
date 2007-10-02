"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from twirlip.model import *

def notification_dropdown(name, selected=None):
    options = [n.name for n in NotificationMethod.select()]
    options = options_for_select(options, selected)
    return select(name, options)

def yes_no_dropdown(name, yes=True):
    options = options_for_select(["Yes", "No"], yes and "Yes" or "No")
    return select(name, options)
