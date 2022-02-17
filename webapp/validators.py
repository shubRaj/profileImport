from django.core.exceptions import ValidationError
from django.utils import timezone
def validate_DOB(value):
    age = timezone.now().year -value.year
    if age<18:
        raise ValidationError(f"Must be older than 18.")