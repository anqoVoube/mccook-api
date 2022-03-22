from apps.recipe.models.recipe import Recipe
from apps.recipe.models.recipe_steps import RecipeSteps
from apps.recipe.serializers.recipe_steps import RecipeStepsSerializer
from rest_framework import serializers 

class RecipeUpdateSerializer(serializers.ModelSerializer):
    # PREFETCH_FIELDS = ['ingredients']
    # RELATED_FIELDS = ['by_cook']

    step_of_recipe = RecipeStepsSerializer(many=True,
                                           required=False)
    # ingredients = serializers.StringRelatedField(many=True,
    #                                              read_only=True)
    class Meta:
        model = Recipe
        fields = ['recipe_id', 'name', 'description', 'step_of_recipe']

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
                'step_of_recipe': steps
        }
    
    def update(self, instance, validated_data):
        steps = validated_data.pop("step_of_recipe", instance.step_of_recipe)
        recipe_itself = super().update(instance, validated_data)
        recipe_steps = [RecipeSteps(
            step_number = step['step_number'],
            description = step['description'],
            recipe = recipe_itself) for step in steps] # Preparing ready-list
        # using list comprehensions for objects to bulk_create

        steps_length = len(recipe_steps)
        objects = RecipeSteps.objects.bulk_create(recipe_steps)
        recipesteps_ids = [objects[step].id for step in range(steps_length)]
        RecipeSteps.objects\
            .filter(recipe=recipe_itself)\
                .exclude(id__in = recipesteps_ids)\
                    .delete()
        return recipe_itself