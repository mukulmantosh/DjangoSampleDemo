from rest_framework import serializers
from django.core.validators import MaxLengthValidator, EmailValidator, ValidationError
from companies.models import EmployeeModel


class CompanySignupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, validators=[MaxLengthValidator(255)])
    founded_by = serializers.CharField(required=True,
                                       validators=[MaxLengthValidator(255)])
    is_certified = serializers.IntegerField(required=True, max_value=1, min_value=0)

