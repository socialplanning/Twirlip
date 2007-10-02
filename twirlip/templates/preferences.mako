<form method="POST">

<p>Please set your notification preferences.  Openplans has many kinds
of events, and you can choose to be notified or not notified for each
of them.</p>

<p>Subscribe me to events automatically when:</p>

<table style="width:50%; border:1px dashed black;">
<tr>
<th style="text-align:left;">Situation</th>
<th style="text-align:left;">Subscribe me</th>
</tr>
% for awc, auto in c.user.all_auto_watch_preferences():
<tr>
  <td>
    ${awc.display_name}
  </td>
  <td>
    ${h.yes_no_dropdown("awc_" + awc.name, auto)}
  </td>
</tr>
% endfor
</table>


<p>For new objects I subscribe to:</p>

<table style="width:50%; border:1px dashed black;">
<tr>
<th style="text-align:left;">Type of event</th>
<th style="text-align:left;">Preferred notification type</th>
</tr>
% for preference in c.user.event_preferences:
<tr>
  <td>
    ${preference.event_class.display_name % "object"}
  </td>
  <td>
    ${h.notification_dropdown("ec_" + preference.event_class.name, selected=preference.notification_method.name)}
  </td>
</tr>
% endfor
</table>

% if len(c.user.url_preferences):
<p>Objects I'm now subscribed to:</p>
<table style="width:50%; border:1px dashed black;">
<tr>
<th style="text-align:left;">Name</th>
<th style="text-align:left;">Preferred notification type</th>
</tr>
% for preference in c.user.url_preferences:
<tr>
  <td>
    ${preference.event_class.display_name % "object"}
  </td>
  <td>
    ${h.notification_dropdown("ec_" + preference.event_class.name, selected=preference.notification_method.name)}
  </td>
</tr>
% endfor
</table>
% endif

<br/>
<input type="submit" name="submit" value="Submit">
</form>