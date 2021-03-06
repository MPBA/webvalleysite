from django.conf.urls import patterns, url

urlpatterns = patterns('applicationprocess.views',
    url(r'^$', 'home'),
    url(r'^set-application-process/$', 'set_application_process'),
    #url(r'^form-test/$', 'form_test'),
    url(r'^edit-form/(?P<form_id>\d+)/$', 'form_edit'),
    url(r'^submit-form/(?P<form_id>\d+)/$', 'submit_signed'),
    url(r'^submit/$', 'submit'),
    url(r'^closed/$', 'closed'),
)

urlpatterns += patterns('applicationprocess.submissions',
    url(r'^admin/csv/(?P<app_status_pk>\d+)/$', 'csv_summary'),
    url(r'^admin/json/(?P<app_status_pk>\d+)/$', 'json_summary'),
)
