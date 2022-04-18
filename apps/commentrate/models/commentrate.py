from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentRate(models.Model):
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
    content_type = models.ForeignKey(ContentType, models.CASCADE, 'comments')
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField()
