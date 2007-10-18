<%inherit file="base.mako"/>
% if c.watches:

<form method="POST">
<input name="done_url" value="${c.done_url}" type="hidden" />

 <div id="watch_table"
      class="oc-widget oc-widget-dataTable oc-clearAfter">
   <h2 class="oc-toggleFold oc-dataTable-heading">
     Pages you are watching (<span id="num_watches">${len(c.watches)})</span>
   </h2>      

<table class="oc-datatable" cellpadding="0" cellspacing="0">
<thead>
  <tr>
    <th class="oc-columnAction" scope="col"></th>
    <th class="oc-columnSortable" scope="col">Name</th>
    <th class="oc-columnAction" scope="col">Actions</th>

  </tr>
</thead>
<tbody>

% for preference in c.watches:
<tr id="up_${preference.id}">
  <td>
<input type="checkbox" name="check:list"
                 value="${preference.id}" /></td>
  </td>
  <td class="oc-dataTable-row-title">
    ${h.link_to(preference.page.title, url=preference.page.url)}
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
</div> <!-- watch table -->
<input type="submit" value="Unwatch" name="task|watchlist" class="oc-button oc-chooseThis" />
</form>
% endif