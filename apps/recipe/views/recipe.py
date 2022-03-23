from rest_framework.views import APIView
from apps.recipe.models.recipe import Recipe
from apps.recipe.serializers.recipe import RecipeCreateSerializer, RecipeListSerializer, RecipeRetrieveSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.http import Http404
from rest_framework import filters
from apps.client.models.client import Client

class RecipeCreateView(APIView):
    def post(self, request):
        serializer = RecipeCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeListView(ListAPIView):
    serializer_class = RecipeListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    def get_queryset(self):
        return Recipe.objects.filter(confirmed="A")


class RecipeRetrieveView(APIView):
    def get_object(self, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except:
            raise Http404
        return recipe

    def get(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = RecipeRetrieveSerializer(object, context={'request': request})
        return Response(serializer.data)

class RecipeFavoriteAddView(APIView):
    def get(self, request, pk, format=None):
        client = Client.objects.get(client_user=request.user)
        recipe = Recipe.objects.get(pk=pk)
        client.favorite_recipes.add(recipe)
        message = "Thank you! The recipe was added successfully"
        return Response({"success": [message]})

# from apps.recipe.models.recipe import Recipe
# from apps.recipe.serializers.recipe import RecipeSerializer
# from rest_framework import viewsets
# from rest_framework.response import Response
# from django.http import Http404




# class RecipeView(viewsets.ModelViewSet):
    
#     queryset = Recipe.objects.select_related('by_cook', 'by_cook__client_user').prefetch_related('ingredients').all()
#     serializer_class = RecipeSerializer
        
#     # def get_queryset(self):
#     #     # This method return serializer class
#     #     # which we pass in class method of serializer class
#     #     # which is also return by get_serializer()
#     #     q = super().get_queryset()
#     #     serializer = self.get_serializer()
#     #     return serializer.get_related_queries(q)

