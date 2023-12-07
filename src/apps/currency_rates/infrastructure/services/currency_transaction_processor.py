from currency_rates.domain.entities import CurrencyTransactionEntity
from currency_rates.domain.interfaces import ICurrencyTransactionProcessor
from currency_rates.models.currency_rates import CurrencyRate
from currency_rates.models.currency_transaction import CurrencyTransaction


class CurrencyTransactionProcessor(ICurrencyTransactionProcessor):
    def create_transaction(self, entity: CurrencyTransactionEntity):
        currency_rate = CurrencyRate.objects.filter(id=entity.currency_rate.pk)
        if currency_rate:
            obj = CurrencyTransaction.objects.create(
                user_id=entity.user_pk,
                currency_rate=entity.currency_rate,
                count=entity.count
            )

            return obj

        return None
