from rest_framework.views import APIView
from apps.client.serializers.client import UserSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED


class UserCreateView(APIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=HTTP_400_BAD_REQUEST)
        