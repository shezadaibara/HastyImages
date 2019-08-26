from django.contrib.auth import get_user_model
from .models import Image
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.conf import settings
import datetime
from Utils.minioClient import MC

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image_link = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = [
            "name", "path", "size", "file_type", "timestamp",
            "updated", "uploaded", "active", "token", "make", "model",
            "xDimension", "yDimension", "orientation", "software",
            "flash", "metering_mode", "saturation",
            "sharpness", "contrast", "x_resolution", "y_resolution",
            "aperture_value", "focal_length", "exif_version", "image_link"
        ]

    def get_image_link(self, image):
        minIO = MC.getInstance()
        link = minIO.client.presigned_get_object(minIO.bucket, image.path, datetime.timedelta(days=1))
        return link