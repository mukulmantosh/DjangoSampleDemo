""" Importing Django Rest Framework Libraries and Module Dependencies. """

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from companies.models import CompanyModel, CompanyAdminModel, CompanyEmployee, EmployeeProfile
from CustomAdmin.models import User
from CustomAdmin import custom_permissions
from . import serializers


class CompanySignupAPI(APIView):
    """
    use this endpoint to create new company.
    Companies can only be created by Admins.
    More details can be found in Swagger Docs.

    """
    permission_classes = (IsAuthenticated, custom_permissions.IsSuperUser,)
    serializers_class = serializers.CompanySignupSerializer
    remove_company_serializer_class = serializers.RemoveCompanySerializer

    def post(self, request):
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid():

                try:
                    with transaction.atomic():

                        clean_data = serializer.data
                        name = clean_data["name"]
                        founded_by = clean_data["founded_by"]
                        is_certified = clean_data["is_certified"]

                        # Create new Company.
                        CompanyModel.objects.create(name=name, founded_by=founded_by, is_certified=is_certified)

                    return Response({"status": True, "message": "New Company Created !", "data": None},
                                    status=status.HTTP_201_CREATED)

                except IntegrityError:
                    transaction.rollback()
                    return Response(
                        {"status": False, "message": "We are facing some issues !", "data": None},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(err)  # read error in background.
            return Response({"status": False, "message": "Something went wrong.",
                             "data": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            serializer = self.remove_company_serializer_class(data=request.data)
            if serializer.is_valid() is not True:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)
            clean_data = serializer.data
            company_id = clean_data["company_id"]

            if CompanyModel.objects.filter(id=company_id).exists():
                # remove company.
                CompanyModel.objects.filter(id=company_id).delete()
                return Response({"status": False, "message": "Company Removed !", "data": None},
                                status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "message": "Something went wrong.", "data": None},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(err)  # read err in background.
            return Response({"status": False, "message": "Something went wrong.", "data": None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyAdminSignupAPI(APIView):
    permission_classes = (IsAuthenticated, custom_permissions.IsSuperUser,)
    serializers_class = serializers.CompanyAdminSignupSerializer

    def post(self, request):
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid() is not True:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)

            clean_data = serializer.data
            first_name = clean_data["first_name"]
            last_name = clean_data["last_name"]
            company_id = clean_data["company_id"]
            email = clean_data["email"]
            password = clean_data["password"]

            try:
                with transaction.atomic():
                    # Create new user.
                    user = User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                               password=password, is_company_admin=True, is_active=True)
                    user.set_password(password)
                    user.save()

                    # Associate user to Company Admin.
                    CompanyAdminModel.objects.create(user_id=user.id, company_id=company_id)

                return Response({"status": True, "message": "New Company Admin Created !", "data": None},
                                status=status.HTTP_201_CREATED)
            except IntegrityError as err:
                print(err)  # read err in background.
                transaction.rollback()
                return Response({"status": False, "message": "Something went wrong.", "data": None},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as err:
            print(err)  # read err in background.
            return Response({"status": False, "message": "Something went wrong.", "data": None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeSignupAPI(APIView):
    permission_classes = (IsAuthenticated, custom_permissions.IsSuperUserOrCompanyAdmin,)
    serializers_class = serializers.EmployeeSignupSerializer

    def post(self, request):
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid() is not True:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)
            clean_data = serializer.data
            first_name = clean_data["first_name"]
            last_name = clean_data["last_name"]
            company_id = clean_data["company_id"]
            email = clean_data["email"]
            password = clean_data["password"]
            dob = clean_data["dob"]
            blood_group = clean_data["blood_group"]
            mobile = clean_data["mobile"]
            permanent_address = clean_data["permanent_address"]
            temporary_address = clean_data["temporary_address"]

            try:
                with transaction.atomic():
                    # create new user.
                    user = User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                               password=password, is_active=True, is_employee=True)
                    user.set_password(password)
                    user.save()

                    # create user profile.
                    EmployeeProfile.objects.create(user_id=user.id, dob=dob, blood_group=blood_group, mobile=mobile,
                                                   temporary_address=temporary_address,
                                                   permanent_address=permanent_address)

                    # associate user with company.
                    CompanyEmployee.objects.create(user_id=user.id, company_id=company_id)

                return Response({"status": True, "message": "New Employee Successfully Created !", "data": None},
                                status=status.HTTP_201_CREATED)

            except IntegrityError as err:
                return Response({"status": False, "message": "Something went wrong.", "data": None},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as err:
            return Response({"status": False, "message": "Something went wrong.", "data": None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeProfileEditAPI(APIView):
    permission_classes = (IsAuthenticated, custom_permissions.IsEmployee,)
    serializers_class = serializers.EmployeeProfileSerializer

    def post(self, request):
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid() is not True:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)

            clean_data = serializer.data
            dob = clean_data["dob"]
            blood_group = clean_data["blood_group"]
            mobile = clean_data["mobile"]
            permanent_address = clean_data["permanent_address"]
            temporary_address = clean_data["temporary_address"]

            if EmployeeProfile.objects.filter(user_id=request.user.id).exists():
                # update profile
                EmployeeProfile.objects.filter(user_id=request.user.id).update(dob=dob, blood_group=blood_group,
                                                                               mobile=mobile,
                                                                               permanent_address=permanent_address,
                                                                               temporary_address=temporary_address)
                return Response({"status": True, "message": "Profile Updated !", "data": None},
                                status=status.HTTP_200_OK)

            else:

                return Response({"status": False, "message": "There is no user with this profile.", "data": None},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response({"status": False, "message": "Something went wrong.", "data": False},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveEmployeeAPI(APIView):
    permission_classes = (IsAuthenticated, custom_permissions.IsSuperUserOrCompanyAdmin)
    serializers_class = serializers.RemoveEmployeeSerializer

    def delete(self, request):
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid() is not True:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)

            clean_data = serializer.data
            employee_id = clean_data["employee_id"]
            User.objects.filter(id=employee_id, is_employee=True).delete()
            return Response({"status": True, "message": "Employee Deleted !", "data": None},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            print(err)  # read err in background.
            return Response({"status": False, "message": "Something went wrong.", "data": None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserAPI(APIView):
    def post(self, request):
        return Response({"status": True, "message": "User Registered !"})