<%inherit file="base.mako"/>
<div style="border: thin dashed black;">
% if c.is_watching:

You're watching this page.  <a href="${h.url_for(action='unwatch', url=c.url, qualified=True)}">Stop watching it?</a>

% else:

You're not watching this page.  <a href="${h.url_for(action='watch', url=c.url, qualified=True)}">Watch it?</a>

% endif

</div>
