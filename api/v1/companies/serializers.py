from rest_framework import serializers
from companies.models import CompanyModel
from django.core.validators import MaxLengthValidator, EmailValidator, ValidationError
from api.v1.CustomAdmin import validators

class CompanySignupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, validators=[MaxLengthValidator(255)])
    founded_by = serializers.CharField(required=True,
                                       validators=[MaxLengthValidator(255)])
    is_certified = serializers.IntegerField(required=True, max_value=1, min_value=0)


class CompanyAdminSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    last_name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    company = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True, validators=[EmailValidator, validators.UserEmailExist])
    password = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator])

    def validate_company(self, company):
        if CompanyModel.objects.filter(id=company).exists():
            return company
        else:
            raise ValidationError({"Sorry! This Company does not exist."})


class EmployeeSignupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    company_id = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    password = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    dob = serializers.DateField(required=True)
    blood_group = serializers.ChoiceField(required=True)
    mobile = serializers.CharField(required=True, max_length=10, validators=[MaxLengthValidator(10)])
