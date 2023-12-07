from django.core.exceptions import ObjectDoesNotExist

from stocks.domain.entities import InvestmentStrategyEntity
from stocks.domain.interfaces import IInvestmentStrategyProcessor
from stocks.models.investment_strategy import InvestmentStrategy


class InvestmentStrategyProcessor(IInvestmentStrategyProcessor):
    def create_investment_strategy(
            self,
            entity: InvestmentStrategyEntity
    ) -> InvestmentStrategyEntity | None:
        obj = InvestmentStrategy.objects.create(
            investment_portfolio_id=entity.inv_port_pk,
            subscribe_commission=entity.subscribe_commission,
            revenue_commission=entity.revenue_commission
        )

        return obj if obj else None

    def delete_investment_strategy(
            self,
            pk: int
    ):
        try:
            obj = InvestmentStrategy.objects.get(pk=pk)
            obj.delete()

        except ObjectDoesNotExist:
            raise ValueError(f'Investment strategy obj with id={pk} does not exists')
