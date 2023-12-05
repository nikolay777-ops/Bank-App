import abc

from user.domain.entities import UserEntity


class IContactsProcessor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_contacts_by_pk(self, user_pk: int) -> list[UserEntity]:
        pass

    @abc.abstractmethod
    def add_close_contact(self, from_pk: int, to_pk: int):
        pass

    @abc.abstractmethod
    def delete_close_contact(self, from_pk: int, to_pk: int):
        pass

    @abc.abstractmethod
    def is_close(self, from_pk: int, to_pk: int) -> bool:
        pass

