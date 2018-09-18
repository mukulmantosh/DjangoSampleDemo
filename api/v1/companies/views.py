""" Importing Django Rest Framework Libraries and Module Dependencies. """

# pylint: disable=import-error
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from companies.models import CompanyModel, CompanyAdminModel
from CustomAdmin.models import User
from . import serializers


class CompanySignupAPI(APIView):
    # pylint: disable=too-few-public-methods

    """
    use this endpoint to create new company.
    Companies can only be created by Admins.

    """
    permission_classes = (AllowAny,)
    serializers_class = serializers.CompanySignupSerializer

    def post(self, request):
        """
        :param name: CharField
        :param founded_by: CharField
        :param is_certified: IntegerField
        :return: return description
        """
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


class CompanyAdminSignupAPI(APIView):
    permission_classes = (AllowAny,)
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
            company_id = clean_data["company"]
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
    permission_classes = (AllowAny,)
    serializers_class = serializers.EmployeeSignupSerializer

    def post(self, request):
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid() is not True:
                return Response({"status": False, "message": serializer.errors, "data": None},
                                status=status.HTTP_400_BAD_REQUEST)
            clean_data = serializer.data

        except Exception as err:
            return Response({"status": False, "message": "Something went wrong.", "data": None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
