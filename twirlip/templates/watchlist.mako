<%inherit file="base.mako"/>
% if c.watches:

${h.secure_form(h.url_for(action="unwatch", controller="watch", qualified=True))}

 <div id="watch_table_div"
      class="oc-widget oc-widget-dataTable oc-clearAfter">
   <h2 class="oc-toggleFold oc-dataTable-heading">
     Pages you are watching (<span id="num_watches">${len(c.watches)}</span>)
   </h2>      

<table class="oc-dataTable" cellpadding="0" cellspacing="0" id="watch_table">
<thead>
  <tr>
    <th class="" style="width: 10px;" scope="col"><input class="oc-checkAll" type="checkbox"></th>
    <th class="oc-columnSortable" style="width: 300px;" scope="col">Name</th>
    <th class="oc-columnAction" scope="col">Actions</th>

  </trl>
</thead>
<tbody>

<%namespace name="pref_row" file="_url_preference_row.mako" />  
% for preference in c.watches:
${pref_row.body(preference)}
% endfor
</tbody>
</table>
<ul class="oc-actions oc-dataTable-actions">
  <li>
    <input type="submit"
           name="task|watchlist"
           value="Unwatch"
           class="oc-button oc-chooseThis oc-js-actionButton" />
  </li>
</ul>
</div> <!-- watch table -->
</form>
% endif
