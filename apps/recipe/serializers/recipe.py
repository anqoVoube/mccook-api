from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps
from apps.recipe.serializers.recipe_steps import RecipeStepsSerializer
from rest_framework import serializers 
from django.db.models import Prefetch
from apps.client.models.client import Client
from apps.ingredients.models.ingredients import Ingredients
from apps.commentrate.models.commentrate import CommentRate
from apps.commentrate.serializers.commentrate import CommentrateSerializer


class WordListingField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class RecipeCreateSerializer(serializers.ModelSerializer):

    step_of_recipe = RecipeStepsSerializer(many=True,
                                           required=True)
    ingredients = WordListingField(many=True)
    class Meta:
        model = Recipe
        fields = ['name', 'description',
                  'ingredients', 'step_of_recipe']

    def to_internal_value(self, data):
        errors = {}
        name = data.get('name')
        description = data.get('description')
        ingredients = data.get('ingredients')
        steps = data.get('step_of_recipe')
        if name is None:
            message = "name object is not assigned"
            errors['not_assigned_name'] = [message]
        elif len(name) < 2:
            message = "name object must have at least 2 letters"
            errors['len_error_name'] = [message]

        if description is None:
            message = "description object is not assigned"
            errors['not_assigned_description'] = [message]
        elif isinstance(description, str) and len(description.split()) < 10:
            message = "description object must have at least 10 words"
            errors['min_word_description'] = [message]

        if ingredients is None:
            message = "ingredients object is not assigned"
            errors['not_assigned_ingredients'] = [message]
        elif ingredients == []:
            message = "ingredients list can\'t be empty"
            errors['empty_list_ingredients'] = [message]
        else:   # !Validate ingredient strings (Example: ['M'])
            for ingredient in ingredients:
                try:
                    Ingredients.objects.get(ingredient_name=ingredient)
                except:
                    message = f"Undefined object as {ingredient} \
in Ingredients-list"
                    errors["no_such_ingredient"] = [message]
                    break

        if steps is None:
            message = "steps object is not assigned"
            errors['not_assigned_steps'] = [message]
        elif steps == []:
            message = "steps list can\'t be empty"
            errors['empty_list_steps'] = [message]
        else:
            for step in steps:
                try:
                    step['step_number']
                    step['description']
                except:
                    message = "Incorrect steps. \
It should contain step_number and description"
                    errors['incorrect_steps'] = [message]
                    break
                if len(step.keys()) != 2:
                    errors['incorrect_steps'] = [message]
                    break

        if errors:
            raise serializers.ValidationError(errors)
        return {
                'name': name,
                'description': description,
                'ingredients': ingredients,
                'step_of_recipe': steps
        }

    def validate(self, attrs): 
        return attrs
    
    def create(self, validated_data):
        name = validated_data['name']
        description = validated_data['description']
        by_cook = Client.objects.get(client_user=self.context['request'].user)
        recipe_itself = Recipe.objects.create(name=name,
                                              description=description,
                                              by_cook=by_cook)
        steps = validated_data.pop("step_of_recipe")
        ingredients = validated_data.pop("ingredients")

        recipe_steps = [RecipeSteps(
            step_number = step['step_number'],
            description = step['description'],
            recipe = recipe_itself) for step in steps] # Preparing ready-list
        # using list comprehensions for objects to bulk_create

        objects = RecipeSteps.objects.bulk_create(recipe_steps)

        ingredient_querysets_list = [Ingredients.objects\
            .get(ingredient_name=str(ingredient_name)\
                .capitalize()) for ingredient_name in ingredients]
        
        recipe_itself.ingredients.add(*ingredient_querysets_list)

        return recipe_itself

class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = WordListingField(many=True)
    class Meta:
        model = Recipe
        fields = ['name', 'description',
                  'ingredients']
        

class RecipeRetrieveSerializer(serializers.ModelSerializer):
    comments_and_rates = serializers.SerializerMethodField()
    step_of_recipe = RecipeStepsSerializer(many=True,
                                           required=True)
    ingredients = WordListingField(many=True)
    class Meta:
        model = Recipe
        fields = ['name', 'description',
                  'ingredients', 'step_of_recipe', 'comments_and_rates']
    
    def get_comments_and_rates(self, obj):
        comments_rates = CommentRate.objects.filter(to_recipe=obj)
        serialized_data = CommentrateSerializer(comments_rates, many=True).data
        return serialized_data
