from django.core.exceptions import ObjectDoesNotExist

from stocks.domain.interfaces import IInvestmentStrategySubscriberProcessor
from stocks.models.subscriber import Subscriber


class InvestmentStrategySubscriberProcessor(IInvestmentStrategySubscriberProcessor):
    def add_investment_strategy_subscriber(
            self,
            investment_strategy_pk: int,
            subscriber_pk: int
    ):
        obj = Subscriber.objects.create(
            investment_strategy_pk=investment_strategy_pk,
            subscriber_pk=subscriber_pk
        )

        return obj if obj else None

    def remove_investment_strategy_subscriber(
            self,
            investment_strategy_pk: int,
            subscriber_pk: int
    ):
        try:
            obj = Subscriber.objects.get(
                investment_strategy_pk=investment_strategy_pk,
                subscriber_pk=subscriber_pk
            )
            obj.delete()

        except ObjectDoesNotExist:
            ValueError(f'Investment strategy subscriber \
            inv_str_id={investment_strategy_pk} sub_id={subscriber_pk} does no exists')
