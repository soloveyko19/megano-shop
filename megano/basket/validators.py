from django.core.exceptions import ValidationError
from rest_framework.request import Request


def payment_validator(request: Request):
    message = "Payment validation error"
    try:
        data = request.data
        name = data.get("name")
        number = data.get("number")
        code = data.get("code")
        year = int(data.get("year"))
        month = int(data.get("month"))
        if not (
                len(number) == 16 and
                int(number) % 2 == 0 and
                len(code) == 3 and
                int(code) and
                int(year) in range(2000, 2100) and
                month in range(1, 13) and
                len(name.split()) < 3
        ):
            raise ValidationError(message)
    except Exception:
        raise ValidationError(message)
