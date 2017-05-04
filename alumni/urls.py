from django.conf.urls import patterns, url

urlpatterns = patterns('alumni.views',
    url(r'^$', 'alumni_views'),
)

