import abc
import datetime


class ICurrencyRateDAO(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_all(self, date_of_use: datetime.datetime):
        pass
