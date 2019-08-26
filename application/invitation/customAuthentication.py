from rest_framework import authentication
from rest_framework import exceptions
from invitation.models import Invitation
from django.utils import timezone


class MyCustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.GET.get('access_token')
        if not access_token:
            raise exceptions.AuthenticationFailed('access_token cannot be None')
        try:
            invitation = Invitation.objects.get(token=access_token)
        except Invitation.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such access_token')
        
        if invitation.expires_at < timezone.now():
            raise exceptions.AuthenticationFailed('access_token has expired')

        return (invitation, None)