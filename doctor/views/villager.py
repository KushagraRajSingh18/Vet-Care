from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from doctor.models import Villager
from doctor.serializers import VillagerSerializer
from doctor.utils import build_response
from rest_framework import status

class VillagerCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['doctor'] = request.user.id

        serializer = VillagerSerializer(data=data)
        if serializer.is_valid():
            villager = serializer.save()
            return build_response(
                status=True,
                message="Villager added successfully.",
                data={"villager_id": villager.id, "name": villager.name},
                status_code=status.HTTP_201_CREATED
            )
        return build_response(
            status=False,
            message="Villager creation failed.",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
