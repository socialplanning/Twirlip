<%inherit file="base.mako"/>
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
   <div class="oc-js-liveEdit">
    <div class="oc-js-liveEdit-value oc-js-liveEdit_showForm oc-liveEdit-value oc-directEdit">Yes</div><!-- end .oc-js-liveEdit -->

            <div class="oc-js-liveEdit-editForm oc-liveEdit-editForm oc-js-actionSelect">
    ${h.yes_no_dropdown("awc_" + awc.name, auto)}
                <input type="submit" class="" value="Go"
                       name="task|awc-${awc.name}|change-listing" />
            </div><!-- end .oc-js-liveEdit-editForm -->

     </div><!-- end .oc-js-liveEdit-editForm .oc-js-actionSelect -->
    </div><!-- end .oc-js-liveEdit .oc-js-actionSelect -->
  </td>
</tr>
% endfor
</table>


% if len(c.user.url_preferences):
<p>Objects I'm now subscribed to:</p>
<table style="width:50%; border:1px dashed black;">
<tr>
<th style="text-align:left;">Name</th>
<th style="text-align:left;">Notify</th>
</tr>
% for preference in c.user.url_preferences:
<tr id="up_${preference.id}">
  <td>
    ${preference.page.title}
  </td>
  <td>
      <ul class="oc-actions oc-dataTable-row-actions">
        <li>
          <a class="oc-actionLink oc-js-actionLink"
             href="${h.url_for(controller='watch', action='unwatch', id=preference.id, ajax=1)}">Stop watching</a>
        </li>
      </ul>
  </td>
</tr>
% endfor
</table>
% endif

<br/>

</form>