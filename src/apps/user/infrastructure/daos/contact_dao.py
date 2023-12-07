from user.domain.entities import ContactEntity
from user.domain.interfaces import IContactDAO
from user.models import Contact


class ContactsDAO(IContactDAO):
    def _orm_to_entity(self, orm_obj: Contact) -> ContactEntity:
        entity = ContactEntity(
            from_user_pk=orm_obj.from_user.pk,
            to_user_pk=orm_obj.to_user.pk,
            is_close=False
        )

        return entity

    def fetch_by_user_pk(self, user_pk: int) -> list[ContactEntity]:
        contact_obj_list = Contact.objects.filter(from_user_id=user_pk)
        contact_entity_list = [
            self._orm_to_entity(orm_obj=contact_obj)
            for contact_obj in contact_obj_list
        ]

        return contact_entity_list
