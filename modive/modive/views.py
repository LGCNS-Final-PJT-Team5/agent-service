from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthCheckView(APIView):
    def get(self, request):
        return Response({'code':status.HTTP_200_OK, 'message':"OK"})