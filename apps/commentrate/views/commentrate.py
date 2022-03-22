from rest_framework.views import APIView
from apps.commentrate.models.commentrate import CommentRate
from apps.commentrate.serializers.commentrate import RecipeCommentrateSerializer, ClientCommentrateSerializer
from rest_framework.response import Response
from rest_framework import status

class RecipeCommentrateView(APIView):
    def post(self, request, pk):
        serializer = RecipeCommentrateSerializer(
                        data=request.data,
                        context={"request": request, "recipe_id": pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Rated and commented"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientCommentrateView(APIView):
    def post(self, request, pk):
        serializer = ClientCommentrateSerializer(
            data=request.data,
            context={"request": request, "client_id": pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Rated and commented"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)