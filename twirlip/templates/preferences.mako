<%inherit file="base.mako"/>
<form class="oc-js-expander oc-expander" method="post" action="${h.url_for(qualified=True)}">
   <input name="done_url" value="${c.done_url}" type="hidden"/>
   ${h.hidden_authenticator()}
   <fieldset>
     <legend class="oc-legend-label">
       <a href="${h.url_for(qualified=True)}" class="oc-js-expander_open oc-expanderLink">Notification preferences</a>
    </legend>

<ul class="oc-js-expander-content oc-expander-content oc-plainList">

% for awc, auto in c.user.all_auto_watch_preferences():
<li>
  <input name="awc_${awc.name}" id="awc_${awc.name}" type="checkbox" 
% if auto:
checked="checked"
% endif
>

  <label for="awc_${awc.name}">
Subscribe me to events automatically when ${awc.display_name}
  </label>
</li>
% endfor

<li><input type="submit" value="Change" name="task|preferences" class="oc-button oc-chooseThis"> or <a href="${h.url_for(qualified=True)}" class="oc-js-expander_close">Cancel</a> 
</li>
</ul>

    </fieldset>
</form>
