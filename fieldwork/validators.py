from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_comma_separated_integer_list(value):
    if value % 3 != 0:
        raise ValidationError(
            _('%(value)s is not an add number'),
            params={'value': value},
        )
