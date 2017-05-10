from django.conf.urls import patterns, url

urlpatterns = patterns('alumni.views',
                       url(r'approval/$', 'alumni_approval_view'),
                       url(r'^$', 'alumni_views'),
)

