from rest_framework.views import APIView
from apps.commentrate.models.commentrate import CommentRate
from apps.commentrate.serializers.commentrate import RecipeCommentrateSerializer, ClientCommentrateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.recipe.models.recipe import Recipe
from apps.commentrate.permissions import RateRecipe, RateClient
from apps.client.models.client import Client

class RecipeCommentrateView(APIView):
    permission_classes = [RateRecipe, IsAuthenticated]
    def post(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            self.check_object_permissions(self.request, recipe)
        except:
            return Response({"not_allowed": "You are not allowed to rate yourself"}, status=status.HTTP_403_FORBIDDEN)
        serializer = RecipeCommentrateSerializer(
                        data=request.data,
                        context={"request": request, "recipe_id": pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Rated and commented"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientCommentrateView(APIView):
    permission_classes = [RateClient, IsAuthenticated]
    def post(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            self.check_object_permissions(self.request, client)
        except:
            return Response({"not_allowed": "You are not allowed to rate yourself"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClientCommentrateSerializer(
            data=request.data,
            context={"request": request, "client_id": pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Rated and commented"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteComment(APIView):
    def get_object(self, pk):
        try:
            comment = CommentRate.objects.get(pk=pk)
            self.check_object_permissions(self.request, comment)
        except:
            message = "You are not allowed to perform this action"
            return Response({"forbidden": [message]},
                            status=status.HTTP_403_FORBIDDEN)

        return comment

    def delete(self, request, pk):
        object = self.get_object(pk)
        object.delete()
        message = "Deleted successfully"
        return Response({"success": [message]},
                        status=status.HTTP_204_NO_CONTENT)

        