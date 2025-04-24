from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password

from doctor.models import Doctor
from doctor.utils import build_response

class DoctorLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return build_response(
                status=False,
                message="Email and password are required.",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctor = Doctor.objects.get(email=email)
        except Doctor.DoesNotExist:
            return build_response(
                status=False,
                message="Doctor not found.",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )

        if check_password(password, doctor.password):
            token, created = Token.objects.get_or_create(user=doctor)
            return build_response(
                status=True,
                message="Login successful.",
                data={"user_id": doctor.id, "token": token.key},
                status_code=status.HTTP_200_OK
            )
        else:
            return build_response(
                status=False,
                message="Incorrect password.",
                data=None,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
