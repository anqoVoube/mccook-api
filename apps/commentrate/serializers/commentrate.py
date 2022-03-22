from rest_framework import serializers
from apps.commentrate.models.commentrate import CommentRate
from apps.client.models.client import Client
from apps.recipe.models.recipe import Recipe
from django.db.models import F

class RecipeCommentrateSerializer(serializers.ModelSerializer):
    understandable = serializers.BooleanField(default=True)
    class Meta:
        model = CommentRate
        fields = ['text', 'rate', 'understandable']
    
    def to_internal_value(self, attrs):
        errors = {}
        understandable = attrs.get('understandable', True)
        text = attrs.get('text')
        rate = int(attrs.get('rate'))
        if not (1 <= rate <= 5):
            message = "Rate should be between 1 and 5"
            errors['rate_value_error'] = [message]
        
        if len(text) <= 10:
            message = "Comment must contain at least 3 characters"
            errors['text_length'] = [message]
        elif len(text) > 200:
            message = "Text must have at most 200 characters"
            errors['text_max_length'] = [message]

        if errors:
            raise serializers.ValidationError(errors)
        return {
            "understandable": understandable,
            "text": text,
            "rate": rate
        }

    def create(self, validated_data):
        text = validated_data['text']
        rate = validated_data['rate']
        understandable = validated_data['understandable']
        client = Client.objects.get(client_user=self.context['request'].user)
        recipe = Recipe.objects.get(recipe_id=int(self.context['recipe_id']))
        recipe.client_rated_recipe += F('client_rated_recipe') + 1
        recipe.overall_stars = F('overall_stars') + rate
        if understandable:
            recipe.overall_understood = F('overall_understood') + 1
        else:
            recipe.overall_understood = F('overall_understood')
        recipe.clearness_votes = F('clearness_votes') + 1
        recipe.save(update_fields=['client_rated_recipe',
                                   'overall_stars',
                                   'overall_understood',
                                   'clearness_votes'])
        commentrate_recipe = CommentRate.objects.create(by_client=client,
                                                 text=text,
                                                 rate=rate,
                                                 to_recipe=recipe)
        return commentrate_recipe
        
class ClientCommentrateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentRate
        fields = ['text', 'rate']
    
    def to_internal_value(self, attrs):
        errors = {}
        text = attrs.get('text')
        rate = int(attrs.get('rate'))
        if not (1 <= rate <= 5):
            message = "Rate should be between 1 and 5"
            errors['rate_value_error'] = [message]
        
        if len(text) <= 10:
            message = "Comment must contain at least 3 characters"
            errors['text_length'] = [message]
        elif len(text) > 200:
            message = "Text must have at most 200 characters"
            errors['text_max_length'] = [message]

        if errors:
            raise serializers.ValidationError(errors)
        return {
            "text": text,
            "rate": rate
        }

    def create(self, validated_data):
        text = validated_data['text']
        rate = validated_data['rate']
        client = Client.objects.get(client_user=self.context['request'].user)
        to_client = Client.objects.get(id=int(self.context['client_id']))
        to_client.overall_rated += F('overall_rated') + 1
        to_client.overall_stars = F('overall_stars') + rate
        to_client.save(update_fields=['overall_rated', 'overall_stars'])
        commentrate_client = CommentRate.objects.create(by_client=client,
                                                 text=text,
                                                 rate=rate,
                                                 to_client=to_client)
        return commentrate_client

class CommentrateSerializer(serializers.ModelSerializer):
    by_client = serializers.StringRelatedField()
    class Meta:
        model = CommentRate
        fields = ['by_client', 'text', 'rate']