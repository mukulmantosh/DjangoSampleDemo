""" Importing Django Rest Framework Libraries and Module Dependencies. """

# pylint: disable=import-error
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from companies.models import EmployeeModel, CompanyModel
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
