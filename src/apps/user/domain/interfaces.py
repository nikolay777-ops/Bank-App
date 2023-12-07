import abc

from user.domain.entities import ContactEntity


class IContactDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_by_user_pk(self, user_pk: int) -> list[ContactEntity]:
        pass


class IContactsProcessor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update_contact_entity(self, entity: ContactEntity):
        pass
