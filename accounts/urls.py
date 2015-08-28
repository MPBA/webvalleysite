from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^logout/$', 'logout'),
    url(r'^login/$', 'login'),
    url(r'^signup/$', 'signup'),
    url(r'^confirm/(?P<activation_key>[a-z0-9]+)$', 'confirm'),
)


