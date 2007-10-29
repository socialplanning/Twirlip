<%inherit file="base.mako"/>
% if c.watches:

${h.secure_form(h.url_for(action="unwatch", controller="watch", qualified=True))}

<input name="done_url" value="${c.done_url}" type="hidden"  action="${h.url_for()}" />

 <div id="watch_table"
      class="oc-widget oc-widget-dataTable oc-clearAfter">
   <h2 class="oc-toggleFold oc-dataTable-heading">
     Pages you are watching (<span id="num_watches">${len(c.watches)}</span>)
   </h2>      

<table class="oc-dataTable" cellpadding="0" cellspacing="0" id="">
<thead>
  <tr>
    <th class="" style="width: 10px;" scope="col"><input class="oc-checkAll" type="checkbox"></th>
    <th class="oc-columnSortable" style="width: 200px;" scope="col">Name</th>
    <th class="oc-columnAction" scope="col">Actions</th>

  </trl>
</thead>
<tbody>

% for preference in c.watches:
<tr id="up_${preference.id}">
  <td>
      <input type="checkbox" name="check:list" value="${preference.id}" />
  </td>

  <td class="oc-dataTable-row-title">
    ${h.link_to(preference.page.title, url=preference.page.url)}
  </td>
  <td>
      <ul class="oc-actions oc-dataTable-row-actions">
        <li>
          <a class="oc-actionLink oc-js-actionPost"
             href="${h.secure_url_for(controller='watch', action='unwatch', id=preference.id, ajax=1, qualified=True)}">Stop watching</a>
        </li>
      </ul>
  </td>
</tr>
% endfor
</tbody>
</table>
</div> <!-- watch table -->
<input type="submit" value="Unwatch" name="task|watchlist" class="oc-button oc-chooseThis" />
</form>
% endif