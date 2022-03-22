from rest_framework import serializers
from apps.ingredients.models.ingredients import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['ingredient_name']
    
    def to_internal_value(self, data):
        ingredient_name = data.get('ingredient_name')
        if ingredient_name is None:
            message = "ingredient_name field is required"
            raise serializers.ValidationError({"required": [message]})
        
        return {
            "ingredient_name": ingredient_name
            }

    def validate(self, attrs):
        ingredient_name = attrs.get('ingredient_name')
        ingredient_name = str(ingredient_name).capitalize()
        attrs['ingredient_name'] = str(ingredient_name).capitalize()
        return attrs

    def create(self, validated_data):
        return Ingredients.objects.create(**validated_data)