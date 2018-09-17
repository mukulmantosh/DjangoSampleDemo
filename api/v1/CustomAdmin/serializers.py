from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.validators import EmailValidator, MaxLengthValidator
from . import validators

class AdminSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, validators=[MaxLengthValidator(255)])
    last_name = serializers.CharField(required=True,
                                      validators=[MaxLengthValidator(255)])
    email = serializers.EmailField(required=True,
                                   validators=[EmailValidator, validators.UserEmailExist, MaxLengthValidator(255)])
    password = serializers.CharField(max_length=255, required=True)

    def validate_password(self, password):
        try:
            password_validation.validate_password(password)
            return password
        except:
            raise ValidationError("Password should contain uppercase,lowercase letters, numbers and special characters."
                                  " At least 8 characters needed.")

