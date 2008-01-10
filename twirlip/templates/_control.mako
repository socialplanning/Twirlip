<div class="oc-boxy" id="twirlip_control">
<form method="POST">

% if c.is_watching:

You're watching this page.  <a href="${h.secure_url_for(action='unwatch', url=c.url, qualified=True)}" class="oc-actionLink oc-js-actionPost">Stop watching it?</a>

% else:

You're not watching this page.  <a href="${h.secure_url_for(action='watch', url=c.url, qualified=True)}" class="oc-actionLink oc-js-actionPost">Watch it?</a>

% endif
</form>
</div>
