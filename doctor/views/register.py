from rest_framework.views import APIView
from doctor.serializers import DoctorRegistrationSerializer
from doctor.models import Doctor
from rest_framework import status
from doctor.utils import build_response

class DoctorRegisterView(APIView):
    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            return build_response(
                status=True,
                message="Doctor registered successfully.",
                data={"user_id": doctor.id},
                status_code=status.HTTP_201_CREATED
            )
        return build_response(
            status=False,
            message="Registration failed.",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
