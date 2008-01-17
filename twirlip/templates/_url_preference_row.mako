<%page args="preference"/>

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
