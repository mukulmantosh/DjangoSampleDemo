from django.core.validators import ValidationError
from CustomAdmin.models import User


def UserEmailExist(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Sorry ! This e-mail address has been already taken.")
    else:
        return email
