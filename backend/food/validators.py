from django.core.exceptions import ValidationError


def validate_not_negativ_value(value):
    if value < 0:
        raise ValidationError('Значение не может быть отрицательным!')