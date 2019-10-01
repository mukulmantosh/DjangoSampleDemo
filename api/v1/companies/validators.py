from django.core.validators import ValidationError
from companies.models import CompanyModel
from rest_framework.views import APIView


def companyExist(company):
    """
    Checks whether the company exists or not in the database
    """
    
    if CompanyModel.objects.filter(id=company).exists():
        return company
    else:
        raise ValidationError("Sorry! This Company does not exist.")

