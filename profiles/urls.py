from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^my/$', 'my'),
    url(r'^edit/$', 'edit'),
    url(r'^browse_applications/(?P<url>.*)$', 'browse_applications', name='browse_applications'),
    url(r'^downloadzip/(?P<dir>.*)/(?P<name>.*)$', 'download_zip', name='download_zip')
)