from django.db import models
import uuid


class DevelopedModel(models.Model):
    created_at = models.DateField('ایجاد شده در', auto_now_add=True)
    updated_at = models.DateTimeField('اپدیت شده در', auto_now=True)
    uuid = models.UUIDField('uuid کد', default=uuid.uuid4,
                            editable=False, unique=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return str(self.uuid)
