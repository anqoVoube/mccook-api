from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Q



class CommentRate(models.Model):

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(to_client__isnull=False,
                        to_recipe=None) | Q(to_client=None,
                                            to_recipe__isnull=False),
                name='not_both_null' #Either to client or recipe
            )
        ]

    by_client = models.ForeignKey('client.Client', 
                                  on_delete=models.CASCADE,
                                  related_name="comment_by")
    text = models.CharField(max_length=200,
                            validators=[MinLengthValidator(10)],
                            blank=False, null=False)
    rate = models.SmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)],
        null=True,
        blank=True)
    to_client = models.ForeignKey('client.Client', 
                                  on_delete=models.CASCADE,
                                  null=True, 
                                  blank=True,
                                  related_name="comment_to_client")
    to_recipe = models.ForeignKey('recipe.Recipe', 
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=True,
                                  related_name="comment_for_recipe")

    def __str__(self):
        if self.to_client is None:
            return 'Comment in {} - recipe: By {}'.format(
                str(self.to_recipe), str(self.by_client))
        return 'Comment in {} - client: By {}'.format(
            str(self.to_client), str(self.by_client))
