from django.utils.translation import gettext_lazy as _
from django.db import models

__all__ = (
    'Contact',
)


class Contact(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='from_contact_user')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='to_contact_user')
    is_close = models.BooleanField(default=False)

    def __str__(self):
        return f'Contact: {self.from_user.name} -> {self.to_user.name}'

    class Meta:
        app_label = 'user'
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        unique_together = ('from_user', 'to_user')
