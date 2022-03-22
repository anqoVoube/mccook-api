from rest_framework import serializers
from apps.recipe.models.recipe_steps import RecipeSteps


class RecipeStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeSteps
        fields = ['step_number', 'description']
    
    # def to_representation(self, value):
    #     return f'{value.step_number}. {value.description}'