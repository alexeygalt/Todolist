from rest_framework.exceptions import ValidationError


def min_length(data):
    if len(data) < 1:
        return ValidationError("Поле не должно быть пустым")
