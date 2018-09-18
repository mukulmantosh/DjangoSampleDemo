from django.db import models
from CustomAdmin.models import User


class DataModel(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CompanyModel(DataModel):
    founded_by = models.CharField(max_length=255)
    is_certified = models.BooleanField(default=False)


class CompanyAdminModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'company')


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    blood_group = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    permanent_address = models.TextField(max_length=500)
    temporary_address = models.TextField(max_length=500)


class CompanyEmployee(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'company')
