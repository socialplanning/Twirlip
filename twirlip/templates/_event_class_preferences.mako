
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
