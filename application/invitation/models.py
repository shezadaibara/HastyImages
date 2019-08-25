from django.db import models
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
import uuid


class Invitation(models.Model):
    """
    Model that is used to store all the Invitation requests. 
    """
    token = models.UUIDField(verbose_name=_('Token'), default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=100, null=False)
    created_at = models.DateTimeField(verbose_name=_('Create Date'), auto_now=True)
    updated_at = models.DateTimeField(verbose_name=_('Update Date'), auto_now=True)
    expires_at = models.DateTimeField(verbose_name=_('Expire Date'))

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")

    def __str__(self):
        return "Invite for {} - {}".format(self.email, self.expires_at)
