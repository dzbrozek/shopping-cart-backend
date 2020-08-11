import uuid

from django.db import models


class Uuidable(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True
