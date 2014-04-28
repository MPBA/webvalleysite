from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^logout/$', 'logout'),
    url(r'^login/$', 'login'),
    url(r'^signup/$', 'signup'),
    url(r'^confirm/(?P<activation_key>[a-z0-9]+)$', 'confirm'),
    url(r'^browse_applications/(?P<url>.*)$', 'browse_applications', name='browse_applications'),
    url(r'^downloadzip/(?P<dir>.*)/(?P<name>.*)$', 'download_zip', name='download_zip')
)


