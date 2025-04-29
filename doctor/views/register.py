import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db import IntegrityError, DatabaseError
from doctor.serializers import DoctorRegistrationSerializer
from doctor.utils import build_response

logger = logging.getLogger(__name__)

class DoctorRegisterView(APIView):
    throttle_scope = 'doctor_register'

    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                doctor = serializer.save()
                token, _ = Token.objects.get_or_create(user=doctor)

                logger.info(
                    f"[REGISTER SUCCESS] Doctor ID={doctor.id}, Email={doctor.email}"
                )

                return build_response(
                    status=True,
                    message="Doctor registered successfully.",
                    data={
                        "user_id": doctor.id,
                        "email": doctor.email,
                        "token": token.key
                    },
                    status_code=status.HTTP_201_CREATED
                )

            except IntegrityError as e:
                logger.warning(
                    f"[DUPLICATE ERROR] Likely duplicate email or phone. Payload={request.data}, Error={str(e)}"
                )
                return build_response(
                    status=False,
                    message="Duplicate entry detected. This email or phone number may already be registered.",
                    data={"details": str(e)},
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            except DatabaseError as e:
                logger.error(f"[DATABASE ERROR] Unexpected DB error: {str(e)}")
                return build_response(
                    status=False,
                    message="A database error occurred. Please contact support if this continues.",
                    data={"error": str(e)},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            except Exception as e:
                logger.critical(f"[UNCAUGHT ERROR] {str(e)}", exc_info=True)
                return build_response(
                    status=False,
                    message="An unexpected error occurred.",
                    data={"error": str(e)},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        logger.warning(
            f"[VALIDATION FAILED] Errors={serializer.errors}, Input={request.data}"
        )
        return build_response(
            status=False,
            message="Invalid input data. Please correct the errors and try again.",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
