""" Importing Django Rest Framework Libraries and Module Dependencies. """

# pylint: disable=import-error
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError

from CustomAdmin.models import User
from . import serializers


class AdminSignupAPI(APIView):
    # pylint: disable=too-few-public-methods

    """
    use this endpoint to create new Admin.

    """
    permission_classes = (AllowAny,)
    serializers_class = serializers.AdminSignupSerializer

    def post(self, request):
        """
        :param first_name: CharField
        :param last_name: CharField
        :param email: EmailField
        :param password: CharField
        :return: return description
        """
        try:
            serializer = self.serializers_class(data=request.data)
            if serializer.is_valid():

                try:
                    with transaction.atomic():

                        clean_data = serializer.data
                        first_name = clean_data["first_name"]
                        last_name = clean_data["last_name"]
                        email = clean_data["email"]
                        password = clean_data["password"]

                        # Create new Admin.
                        user = User.objects.create(first_name=first_name, last_name=last_name,
                                                   email=email, password=password, is_active=True,
                                                   is_superuser=True)

                        user.set_password(password)
                        user.save()

                    return Response({"status": True, "message": "Admin Created !", "data": None},
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
