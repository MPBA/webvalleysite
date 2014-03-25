from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^my/$', 'my'),
    url(r'^edit/$', 'edit'),
)