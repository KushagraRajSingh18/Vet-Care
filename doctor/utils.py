from rest_framework.response import Response

def build_response(status: bool, message: str, data=None, status_code=200):
    return Response({
        "status": status,
        "message": message,
        "data": data
    }, status=status_code)  