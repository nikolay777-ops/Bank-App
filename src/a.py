import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django

django.setup()

from remittance.models.remittance import Remittance
from remittance.infrastructure.services.remittance_processor import RemittanceProcessor
processor = RemittanceProcessor()
obj = Remittance.objects.all()
obj = obj[0]
processor.accept_remittance(remittance_pk=obj.pk)