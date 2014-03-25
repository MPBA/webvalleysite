from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

validate_country_code = RegexValidator( '^[a-z]{2}-[A-Z]{2}$', _( 'Enter a valid country code.' ))