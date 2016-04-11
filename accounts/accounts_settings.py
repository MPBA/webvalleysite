from django.conf import settings

#### Default number of news per page
WEBVALLEY_EMAIL_ADDRESS = getattr(settings, "EMAIL_ADDRESS", "webvalley@fbk.eu")

CONFIRMATION_EMAIL_SUBJECT = getattr(settings, "CONFIRMATION_EMAIL_SUBJECT", "WebValley account confirmation")
CONFIRMATION_EMAIL_TEMPLATE = getattr(settings, "CONFIRMATION_EMAIL_TEMPLATE", "email/account_confirmation.html")
