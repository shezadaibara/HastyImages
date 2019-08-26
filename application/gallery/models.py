from django.db import models
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
import uuid

class Gallery(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, null=False, default=0)
    token = models.CharField(verbose_name=_('Token'), max_length=100, null=True, blank=True, editable=False, db_index=True)
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
    token = models.CharField(verbose_name=_('Token'), max_length=100, null=True, blank=True, editable=False, db_index=True)

    make= models.CharField(max_length=50, null=True, blank=True)
    model= models.CharField(max_length=50, null=True, blank=True)
    xDimension= models.IntegerField(null=True, blank=True)
    yDimension= models.IntegerField(null=True, blank=True)
    orientation= models.IntegerField(null=True, blank=True)
    software = models.CharField(max_length=50, null=True, blank=True)
    flash = models.CharField(max_length=150, null=True, blank=True)
    metering_mode = models.CharField(max_length=50, null=True, blank=True)
    saturation = models.CharField(max_length=50, null=True, blank=True)
    sharpness = models.CharField(max_length=50, null=True, blank=True)
    contrast = models.CharField(max_length=50, null=True, blank=True)
    x_resolution = models.CharField(max_length=50, null=True, blank=True)
    y_resolution = models.CharField(max_length=50, null=True, blank=True)
    aperture_value = models.CharField(max_length=50, null=True, blank=True)
    focal_length = models.CharField(max_length=50, null=True, blank=True)
    exif_version= models.CharField(max_length=50, null=True, blank=True)

    @property
    def title(self):
        return str(self.name)