import datetime
from django.core.exceptions import ValidationError


def time_validation(data):
    print(data)
    if data > datetime.date.today().year:
        raise ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли.'
        )
    return data
