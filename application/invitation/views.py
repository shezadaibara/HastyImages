from django.shortcuts import render
from rest_framework import viewsets
from .serializers import InvitationSerializer
from invitation.models import Invitation
from rest_framework.response import Response


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all().order_by('-created_at')
    serializer_class = InvitationSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            response = super(InvitationViewSet, self).create(
                request, *args, **kwargs)
        except Exception as e:
            response = Response({"error_message": str(e)}, status=409)

        return response