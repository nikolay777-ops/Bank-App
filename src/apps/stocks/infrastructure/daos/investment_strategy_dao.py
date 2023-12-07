from stocks.domain.entities import InvestmentStrategyEntity
from stocks.domain.interfaces import IInvestmentStrategyDAO
from stocks.models.investment_strategy import InvestmentStrategy


class InvestmentStrategyDAO(IInvestmentStrategyDAO):
    def _orm_to_entity(self, orm_obj: InvestmentStrategy) -> InvestmentStrategyEntity:
        entity = InvestmentStrategyEntity(
            inv_port_pk=orm_obj.investment_portfolio.pk,
            subscribe_commission=orm_obj.subscribe_commission,
            revenue_commission=orm_obj.revenue_commission
        )

        return entity

    def fetch_all_by_user_pk(
            self,
            user_pk: int
    ) -> list[InvestmentStrategyEntity]:
        strategy_obj_list = InvestmentStrategy.objects.filter(investment_portfolio__owner_id=user_pk)

        strategies_entity_list = [
            self._orm_to_entity(orm_obj=strategy_obj)
            for strategy_obj in strategy_obj_list
        ]

        return strategies_entity_list
