from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from utilities.common_abstract_models import BaseAbstract


class Chat(BaseAbstract):
    name = models.CharField(
        verbose_name="Name",
        max_length=255,
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from='name',
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Chat, self).save(*args, **kwargs)

    class Meta:
        db_table = 'chat'
        ordering = ('-created_at',)
