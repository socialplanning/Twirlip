Twirlip accepts Cabochon messages repesenting page creation and edits,
and sends email to people subscribed to these events.  It also
provides an interface for subscription/unsubscription, which is
intended to be transcluded (or maybe scripttranscluded) into Opencore,
although it could be used more broadly.


Installation and Setup
======================

Install ``Twirlip`` using easy_install::

    easy_install Twirlip

Make a config file as follows::

    paster make-config Twirlip config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
