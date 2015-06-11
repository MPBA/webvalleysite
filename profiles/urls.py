from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^my/$', 'my'),
    url(r'^edit/$', 'edit'),
    url(r'^test/$', 'test_view'),
    url(r'^browse_applications/(?P<url>.*)$', 'browse_applications', name='browse_applications'),
    url(r'^browse_papers/(?P<url>.*)$', 'browse_paper', name='browse_papers'),
    url(r'^del_papers/(?P<myurl>.*)/(?P<mydir>.*)/$', 'remove_file', name='del_paper'),
    url(r'^create_dir/(?P<url>.*)/$', 'make_dir', name='create_dir'),
    url(r'^downloadzip/(?P<dir>.*)/(?P<name>.*)$', 'download_zip', name='download_zip')
)