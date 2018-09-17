from django.db import models


class DataModel(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CompanyModel(DataModel):
    founded_by = models.CharField(max_length=255)
    is_certified = models.BooleanField(default=False)


class EmployeeModel(DataModel):
    company = models.OneToOneField(CompanyModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    dob = models.DateField()
    blood_group = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)


