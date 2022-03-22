from rest_framework.views import APIView
from apps.client.serializers.client import UserSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from apps.client.serializers.client import ClientRetrieveSerializer
from apps.client.models.client import Client
from django.http import Http404
from rest_framework import status


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

class ClientRetrieveView(APIView):
    serializer_class = ClientRetrieveSerializer
    def get_object(self, pk):
        try:
            client = Client.objects.get(pk=pk)
        except:
            raise Http404
        return client

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
        