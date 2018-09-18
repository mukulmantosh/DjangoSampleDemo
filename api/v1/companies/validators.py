from django.core.validators import ValidationError
from companies.models import CompanyModel


def companyExist(self, company):
    if CompanyModel.objects.filter(id=company).exists():
        return company
    else:
        raise ValidationError({"Sorry! This Company does not exist."})
