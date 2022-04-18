import os
from django.db.models import (Model,
                              ForeignKey,
                              CASCADE,
                              CharField,
                              PositiveIntegerField,
                              ImageField)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def get_upload_path(instance, filename):
    return os.path.join(f'{instance.content_type.model}', f'{instance.object_id}', filename)


class Image(Model):
    content_type = ForeignKey(ContentType, CASCADE, 'attachments')
    content_object = GenericForeignKey('content_type', 'object_id', )
    object_id = PositiveIntegerField()
    file = ImageField(upload_to=get_upload_path)
