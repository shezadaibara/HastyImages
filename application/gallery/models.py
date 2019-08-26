from django.db import models
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
import uuid

class Gallery(models.Model):
    token = models.UUIDField(verbose_name=_('Token'), default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(verbose_name=_('Name'), null=True, max_length=50)
    created_at = models.DateTimeField(verbose_name=_('Create Date'), auto_now=True)
    updated_at = models.DateTimeField(verbose_name=_('Update Date'), auto_now=True)

    def __str__(self):
        return "Gallery {} - {}".format(self.name, self.created_at)


class Image(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    gallery = models.ForeignKey(
        Gallery, related_name='Image',
        on_delete=models.CASCADE, verbose_name=_("Gallery")
        )

    @property
    def title(self):
        return str(self.name)