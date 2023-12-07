import datetime
from abc import ABC

from currency_rates.domain.entities import CurrencyRateEntity
from currency_rates.domain.interfaces import ICurrencyRateDAO
from currency_rates.models.currency_rates import CurrencyRate
from django.db.models import Window, F
from django.db.models.functions import Rank


class CurrencyRatesDAO(ICurrencyRateDAO, ABC):
    def _orm_to_entity(self, orm_object: CurrencyRate) -> CurrencyRateEntity:
        currency_rate_entity = CurrencyRateEntity(
            currency=orm_object.currency.name,
            rate=orm_object.rate,
            date_of_use=orm_object.date_of_use,
        )

        return currency_rate_entity

    def fetch_latest_all(self) -> list[CurrencyRateEntity]:
        # Annotate the CurrencyRate instances with a rank in descending order of date_of_use for each currency
        currency_rates = CurrencyRate.objects.annotate(
            rank=Window(
                expression=Rank(),
                partition_by=[F('currency')],
                order_by=F('date_of_use').desc()
            )
        )

        # Filter for the CurrencyRate instances that have the first rank in each partition
        latest_rates = currency_rates.filter(rank=1)

        currency_rate_entity_list = [
            self._orm_to_entity(orm_object=rate)
            for rate in latest_rates
        ]

        return currency_rate_entity_list

    def fetch_latest_by_currency_pk(
            self,
            currency_pk: str
    ) -> CurrencyRateEntity:

        currency_rate = CurrencyRate.objects.filter(currency__id=currency_pk).order_by('-date_of_use')

        entity = None
        if currency_rate:
            entity = self._orm_to_entity(orm_object=currency_rate)

        return entity
