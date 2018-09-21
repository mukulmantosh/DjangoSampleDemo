from rest_framework import serializers
from companies.models import CompanyModel
from django.core.validators import MaxLengthValidator, EmailValidator, ValidationError
from api.v1.CustomAdmin import validators as user_validator
from CustomAdmin.models import User
from . import validators

BLOOD_GROUP = (
    ('A+', 'A+'),
    ('O+', 'O+'),
    ('B+', 'B+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('O-', 'O-'),
    ('B-', 'B-'),
    ('AB-', 'AB-'),

)


class CompanySignupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, validators=[MaxLengthValidator(255)])
    founded_by = serializers.CharField(required=True,
                                       validators=[MaxLengthValidator(255)])
    is_certified = serializers.IntegerField(required=True, max_value=1, min_value=0)


class RemoveCompanySerializer(serializers.Serializer):
    company_id = serializers.IntegerField(required=True)


class CompanyAdminSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    last_name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    company_id = serializers.IntegerField(required=True, validators=[validators.companyExist])
    email = serializers.EmailField(required=True, validators=[EmailValidator, user_validator.UserEmailExist])
    password = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator])


class EmployeeSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    last_name = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    company_id = serializers.IntegerField(required=True, validators=[validators.companyExist])
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    password = serializers.CharField(required=True, max_length=255, validators=[MaxLengthValidator(255)])
    dob = serializers.DateField(required=True)
    blood_group = serializers.ChoiceField(required=True, choices=BLOOD_GROUP)
    mobile = serializers.CharField(required=True, max_length=10, validators=[MaxLengthValidator(10)])
    permanent_address = serializers.CharField(required=True, max_length=500)
    temporary_address = serializers.CharField(required=True, max_length=500)


class EmployeeProfileSerializer(serializers.Serializer):
    dob = serializers.DateField(required=True)
    blood_group = serializers.ChoiceField(required=True, choices=BLOOD_GROUP)
    mobile = serializers.CharField(max_length=10, required=True)
    permanent_address = serializers.CharField(max_length=500, required=True)
    temporary_address = serializers.CharField(max_length=500, required=True)


class RemoveEmployeeSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField(required=True)

    def validate_employee_id(self, employee_id):
        if User.objects.filter(id=employee_id, is_employee=True).exists() is not True:
            raise ValidationError("Sorry! We did not find any employee.")
        else:
            return employee_id
