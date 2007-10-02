from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1191361446.8411331
_template_filename='/home/novalis/tasktracker/src/Twirlip/twirlip/templates/preferences.mako'
_template_uri='/preferences.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<form method="POST">\n\n<p>Please set your notification preferences.  Openplans has many kinds\nof events, and you can choose to be notified or not notified for each\nof them.</p>\n\n<p>Subscribe me to events automatically when:</p>\n\n<table style="width:50%; border:1px dashed black;">\n<tr>\n<th style="text-align:left;">Situation</th>\n<th style="text-align:left;">Subscribe me</th>\n</tr>\n')
        # SOURCE LINE 14
        for awc, auto in c.user.all_auto_watch_preferences():
            # SOURCE LINE 15
            context.write(u'<tr>\n  <td>\n    ')
            # SOURCE LINE 17
            context.write(unicode(awc.display_name))
            context.write(u'\n  </td>\n  <td>\n    ')
            # SOURCE LINE 20
            context.write(unicode(h.yes_no_dropdown("awc_" + awc.name, auto)))
            context.write(u'\n  </td>\n</tr>\n')
        # SOURCE LINE 24
        context.write(u'</table>\n\n\n<p>For new objects I subscribe to:</p>\n\n<table style="width:50%; border:1px dashed black;">\n<tr>\n<th style="text-align:left;">Type of event</th>\n<th style="text-align:left;">Preferred notification type</th>\n</tr>\n')
        # SOURCE LINE 34
        for preference in c.user.event_preferences:
            # SOURCE LINE 35
            context.write(u'<tr>\n  <td>\n    ')
            # SOURCE LINE 37
            context.write(unicode(preference.event_class.display_name % "object"))
            context.write(u'\n  </td>\n  <td>\n    ')
            # SOURCE LINE 40
            context.write(unicode(h.notification_dropdown("ec_" + preference.event_class.name, selected=preference.notification_method.name)))
            context.write(u'\n  </td>\n</tr>\n')
        # SOURCE LINE 44
        context.write(u'</table>\n\n')
        # SOURCE LINE 46
        if len(c.user.url_preferences):
            # SOURCE LINE 47
            context.write(u'<p>Objects I\'m now subscribed to:</p>\n<table style="width:50%; border:1px dashed black;">\n<tr>\n<th style="text-align:left;">Name</th>\n<th style="text-align:left;">Preferred notification type</th>\n</tr>\n')
            # SOURCE LINE 53
            for preference in c.user.url_preferences:
                # SOURCE LINE 54
                context.write(u'<tr>\n  <td>\n    ')
                # SOURCE LINE 56
                context.write(unicode(preference.event_class.display_name % "object"))
                context.write(u'\n  </td>\n  <td>\n    ')
                # SOURCE LINE 59
                context.write(unicode(h.notification_dropdown("ec_" + preference.event_class.name, selected=preference.notification_method.name)))
                context.write(u'\n  </td>\n</tr>\n')
            # SOURCE LINE 63
            context.write(u'</table>\n')
        # SOURCE LINE 65
        context.write(u'\n<br/>\n<input type="submit" name="submit" value="Submit">\n</form>')
        return ''
    finally:
        context.caller_stack.pop_frame()


