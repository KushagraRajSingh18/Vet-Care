from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from doctor.models import Animal
from doctor.serializers import AnimalSerializer
from doctor.utils import build_response
from rest_framework import status

class AnimalCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnimalSerializer(data=request.data)
        if serializer.is_valid():
            animal = serializer.save()
            return build_response(
                status=True,
                message="Animal added successfully.",
                data={"animal_id": animal.id, "species": animal.species},
                status_code=status.HTTP_201_CREATED
            )
        return build_response(
            status=False,
            message="Animal creation failed.",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
