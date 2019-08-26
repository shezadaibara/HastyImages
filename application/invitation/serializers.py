from django.contrib.auth import get_user_model
from invitation.models import Invitation
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class InvitationSerializer(serializers.HyperlinkedModelSerializer):
    upload_link = serializers.SerializerMethodField()
    class Meta:
        model = Invitation
        fields = ('token', 'email', 'created_at', 'updated_at', 'expires_at', 'upload_link')
        extra_kwargs = {
                        'email': {"required": True},
                        'expires_at': {"required": False}
                        }

    def create(self, validated_data):
        default = {
            "expires_at" : timezone.now() + settings.DEFAULT_TOKEN_EXPIRE_TIMESPAN
        }
        invitation, created = Invitation.objects.get_or_create(
            email=validated_data.get('email'), defaults=default)
        if not created:
            invitation.expires_at = default['expires_at']
            invitation.updated_at = timezone.now()
            invitation.save()
        return invitation

    def get_upload_link(self, invitation):
        request = self.context.get('request')
        link =  "{url}?access_token={token}".format(url=reverse('upload-home'), token=invitation.token)
        return request.build_absolute_uri(link)


