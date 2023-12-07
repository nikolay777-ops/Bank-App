from currency_rates.domain.entities import CurrencyRateEntity
from currency_rates.domain.interfaces import ICurrencyRateProcessor
from currency_rates.models.currency_rates import CurrencyRate


class CurrencyRateProcessor(ICurrencyRateProcessor):
    def create_currency_rate(self, entity: CurrencyRateEntity) -> CurrencyRate | None:

        obj = CurrencyRate.objects.create(
            currency_id=entity.currency,
            rate=entity.rate,
            date_of_use=entity.date_of_use
        )

        if obj:
            return obj

        return None
