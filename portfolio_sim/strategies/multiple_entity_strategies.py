import pandas as pd
import numpy as np

from portfolio_sim.strategies.base_strategy import BaseStrategy


class PropMaxSentimentLongStrategy(BaseStrategy):
    """
    Long Strategy, ranks companies by sentiment and buys the amount of money proportional to the sentiment of each company
    """

    def __init__(self):
        super().__init__("PropMaxSentimentLong")
        self.limit = 30

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
        new_portfolio = {company: {"order": 0, "wantToSell": wantToSell} for company in portfolio}
        sentiments = {}
        for company in daily_data:
            if daily_data[company].Volume > 40:
                sentiments[company] = daily_data[company].Sentiment
        sentiments = pd.Series(sentiments, dtype="float64").sort_values(
            ascending=False
        )[: self.limit]
        # Buy company with max sentiment
        if len(sentiments) > 0:
            moneys = (
                (np.arange(len(sentiments)) + 1)
                / (np.arange(len(sentiments)) + 1).sum()
            )[::-1] * money
            for i in range(len(sentiments)):
                new_portfolio[sentiments.index[i]]["order"] += np.floor(
                    moneys[i] / daily_data[sentiments.index[i]].Close
                )
                new_portfolio[sentiments.index[i]]["wantToSell"] = False
        return new_portfolio


class PropMinSentimentShortStrategy(BaseStrategy):
    """
    Short Strategy, ranks companies by sentiment and shorts the amount of money proportional to the sentiment of each company
    """

    def __init__(self):
        super().__init__("PropMinSentimentShort")
        self.limit = 2

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

        new_portfolio = {company: {"order": 0, "wantToSell": wantToSell} for company in portfolio}
        sentiments = {}
        for company in daily_data:
            if daily_data[company].Volume > 40:
                sentiments[company] = daily_data[company].Sentiment
        sentiments = pd.Series(sentiments, dtype="float64").sort_values(ascending=True)[
            : self.limit
        ]
        if len(sentiments) > 0:
            moneys = (
                (np.arange(len(sentiments)) + 1)
                / (np.arange(len(sentiments)) + 1).sum()
            )[::-1] * short_limit
            for i in range(len(sentiments)):
                new_portfolio[sentiments.index[i]]["order"] -= np.floor(
                    moneys[i] / daily_data[sentiments.index[i]].Close
                )
                new_portfolio[sentiments.index[i]]["wantToSell"] = False
        return new_portfolio


class PropMinMaxSentimentStrategy(BaseStrategy):
    """
    Long-Short Strategy, ranks companies by sentiment and buys the amount of money proportional to the sentiment of each company and shorts the amount of money proportional to the sentiment of each company
    """

    def __init__(self):
        super().__init__("PropMinMaxSentiment")
        self.limit = 100
        self.short_lim_length = 1

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

        new_portfolio = {company: {"order": 0, "wantToSell": wantToSell} for company in portfolio}
        sentiments = {}
        for company in daily_data:
            if daily_data[company].Volume > 40:
                sentiments[company] = daily_data[company].Sentiment
        if len(sentiments) == 1:
            return new_portfolio
        elif len(sentiments) <= self.limit:
            curr_lim = len(sentiments) - 1
        else:
            curr_lim = self.limit
        long_sentiments = pd.Series(sentiments, dtype="float64").sort_values(
            ascending=False
        )[:curr_lim]
        short_sentiments = pd.Series(sentiments, dtype="float64").sort_values(
            ascending=True
        )[: self.short_lim_length]

        if len(long_sentiments) > 0:
            moneys = (
                (np.arange(len(long_sentiments)) + 1)
                / (np.arange(len(long_sentiments)) + 1).sum()
            )[::-1] * money
            for i in range(len(long_sentiments)):
                new_portfolio[long_sentiments.index[i]]["order"] += np.floor(
                    moneys[i] / daily_data[long_sentiments.index[i]].Close
                )
                new_portfolio[sentiments.index[i]]["wantToSell"] = False
        if len(short_sentiments) > 0:
            moneys = (
                (np.arange(len(short_sentiments)) + 1)
                / (np.arange(len(short_sentiments)) + 1).sum()
            )[::-1] * short_limit
            for i in range(len(short_sentiments)):
                new_portfolio[short_sentiments.index[i]]["order"] -= np.floor(
                    moneys[i] / daily_data[short_sentiments.index[i]].Close
                )
                new_portfolio[sentiments.index[i]]["wantToSell"] = False
        return new_portfolio
