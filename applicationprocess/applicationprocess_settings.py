from django.conf import settings

APP_USER_DATA_ROOT = settings.MEDIA_ROOT#.child( 'userdata' )

USER_DATA_ROOT = getattr( settings, "USER_DATA_ROOT", APP_USER_DATA_ROOT )

APPLICATION_CLOSED_URL = getattr( settings, "APPLICATION_CLOSED_URL", "/school-application/closed/" )

APPLICATIONPROCESS_HANDLER_EMAILS = getattr( settings, "APPLICATIONPROCESS_HANDLER_EMAILS", ( "email@example.com", ) )
APPLICATIONPROCESS_EMAIL_SUBJECT = getattr( settings, "APPLICATIONPROCESS_EMAIL_SUBJECT", "WebValley Application Submitted")


class FormStatusChoices(object):
    INCOMPLETE = 'incomplete'
    FILLED = 'filled'
    COMPLETED = 'completed'

class ApplicationStatusChoices(object):
    ONGOING = 'ongoing'
    NOT_SET = 'not_set'
    WEBVALLEY_STAFF = 'webvalley_staff'
    ALL_FILLED = 'all_filled'


