import pandas as pd

from portfolio_sim.strategies.base_strategy import BaseStrategy


class DefaultDecisionFunction(BaseStrategy):
    """
    Default Decision Function
    """

    def __init__(self):
        super().__init__("Default")

    def get_decision(
        self,
        daily_data: pd.DataFrame,
        portfolio: dict,
        money: float,
        short_limit: float,
        wantToSell: bool,
    ) -> dict:
        """
        Decision Function for Default Strategy
        Args:
            daily_data: Dataframe of daily data containing price information and any other information for each company
            portfolio: Dictionary of number of shares of each company in the portfolio
            money: Available money to invest
            short_limit: Limit of money to invest in short positions
        Returns:
            Dictionary of number of shares to buy or sell for each company
        """
        new_portfolio = portfolio.copy()
        new_money = money
        new_portfolio = {
            company: (new_money / len(new_portfolio)) / daily_data[company].Close
            for company in new_portfolio
        }
        new_money = 0
        return new_portfolio
