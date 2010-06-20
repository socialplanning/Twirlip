<form method="POST" id="twirlip_control">

% if c.is_watching:

<a href="${h.secure_url_for(action='unwatch', url=c.url, qualified=True)}" class="oc-js-actionPost">Unwatch</a>

% else:

<a href="${h.secure_url_for(action='watch', url=c.url, qualified=True)}" class="oc-js-actionPost">Watch</a>

% endif
</form>

