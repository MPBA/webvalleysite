from django.conf.urls import patterns, url

urlpatterns = patterns('timetable.views',
    url(r'^$', 'display'),
)

