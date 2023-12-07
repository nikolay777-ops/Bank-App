from abc import ABC

from django.core.exceptions import ObjectDoesNotExist

from user.domain.entities import ContactEntity
from user.domain.interfaces import IContactsProcessor
from user.models import Contact


class ContactsProcessor(IContactsProcessor, ABC):

    def update_contact_entity(self, entity: ContactEntity):
        try:
            obj = Contact.objects.get(from_user_id=entity.from_user_pk, to_user_id=entity.to_user_pk)
            obj.is_close = entity.is_close
            obj.save()
        except ObjectDoesNotExist:
            raise ValueError(f'Contact with such from_id:{entity.from_user_pk} to_id:{entity.to_user_pk} does not exists')
    
