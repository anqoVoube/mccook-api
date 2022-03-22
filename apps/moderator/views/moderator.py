from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from apps.recipe.models.recipe import Recipe
from apps.moderator.serializers.moderator import RecipeUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Q

class RecipeModeratorRetrieveView(APIView):
    def get_object(self, pk):
        try:
            recipes = Recipe.objects.get(pk = pk)
        except:
            raise Http404
        return recipes

    def get(self, request, pk,format=None):
        get_recipes = self.get_object(pk)
        serializer = RecipeUpdateSerializer(get_recipes)
        return Response(serializer.data)

    def patch(self, request, pk):
        get_recipe = self.get_object(pk)
        # serializer = RecipeUpdateSerializer(get_recipe,
        #                                     data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     message = "The recipe was successfully"
        #     return Response({"success": [message]})
        if request.data['confirmed'] == "A":   # Checking whether we get
            # any other changes 
            if len(request.data.keys()) > 1: #changes were made,
                # because key.count > 1, so do the changes and publish
                serializer = RecipeUpdateSerializer(get_recipe,
                                                    data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    recipe = Recipe.objects.get(pk=pk)
                    recipe.confirmed = "A"
                    recipe.save(update_fields=['confirmed'])
                    message = "The recipe was successfully \
published with changes"
                    return Response({"success": [message]})
            else:   # All good and changes weren't made, just publish.
                recipe = Recipe.objects.get(pk=pk)
                recipe.confirmed = "A"
                recipe.save(update_fields=['confirmed'])
                message = "The recipe was successfully published \
without changes"
                return Response({"success": [message]})

        elif request.data['confirmed'] == "S":
            if len(request.data.keys()) > 1: # Checking whether we get
                # any other changes (changes were made, because key.count > 1)
                serializer = RecipeUpdateSerializer(get_recipe,
                                                    data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    message = "The recipe was saved without publishing"
                    return Response({"success": [message]})
            # Changes weren't made, just return Response, w/out doing anything.
            message = "The recipe wasn\'t changed and not published"
            return Response({"success": [message]})
        elif request.data['confirmed'] == "D":  #delete
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()
            message = "Recipe was successfully deleted"
            return Response({"success": [message]},
                            status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeModeratorListView(ListAPIView):
    serializer_class = RecipeUpdateSerializer
    queryset = Recipe.objects.filter(confirmed="S")