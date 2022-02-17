from django.core.exceptions import ValidationError
from django.utils import timezone
def validate_DOB(value):
    age = timezone.now().year -value.year
    if age<18:
        raise ValidationError(f"Must be older than 18.")
def validate_salary(value):
    if value > 5_00_000:
        raise ValidationError(f"No one's gonna pay you over 5,00,000.")