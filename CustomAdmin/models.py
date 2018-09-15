from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CustomUser(TimeStampModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.first_name

    def __repr__(self):
        return self.__class__.__name__


class Role(TimeStampModel):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = "custom_role"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__class__.__name__


class UserRole(TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "custom_user_role"

    def __str__(self):
        return "{} has been assigned role {}.".format(self.user.first_name, self.role.name)

    def __repr__(self):
        return self.__class__.__name__
