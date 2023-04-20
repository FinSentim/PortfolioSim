import pandas as pd
import numpy as np

from portfolio_sim.strategies.base_strategy import BaseStrategy


class MaxSentimentLongStrategy(BaseStrategy):
    """
    Long Strategy, buys the company with the highest sentiment each day
    """

    def __init__(self):
        super().__init__("MaxSentimentLong")

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
        new_portfolio = {company: {"shares": 0, "wantToSell": wantToSell} for company in portfolio}
        # Get max sentiment among all companies
        max_sentiment = -2
        max_company = None
        for company in daily_data:
            if daily_data[company].Sentiment > max_sentiment:
                if daily_data[company].Volume > 40:
                    max_sentiment = daily_data[company].Sentiment
                    max_company = company
        # Buy company with max sentiment
        if max_company is not None:
            new_portfolio[max_company]["shares"] += np.floor(
                money / daily_data[max_company].Close
            )
            new_portfolio[max_company]["wantToSell"] = False
        return new_portfolio


class MinSentimentShortStrategy(BaseStrategy):
    """
    Short Strategy, shorts the company with the lowest sentiment each day
    """

    def __init__(self):
        super().__init__("MinSentimentShort")

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
        new_portfolio = {company: {"shares": 0, "wantToSell": wantToSell} for company in portfolio}
        # Get max sentiment among all companies
        min_sentiment = 2
        min_company = None
        for company in daily_data:
            if daily_data[company].Sentiment < min_sentiment:
                if daily_data[company].Volume > 40:
                    min_sentiment = daily_data[company].Sentiment
                    min_company = company
        # Buy company with max sentiment
        if min_company is not None:
            new_portfolio[min_company]["shares"] -= np.floor(
                short_limit / daily_data[min_company].Close
            )
            new_portfolio[min_company]["wantToSell"] = False
        return new_portfolio


class MinMaxSentimentStrategy(BaseStrategy):
    """
    Long-Short Strategy, buys the company with the highest sentiment each day and shorts the company with the lowest sentiment each day
    """

    def __init__(self):
        super().__init__("MinMaxSentiment")

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
        new_portfolio = {company: {"shares": 0, "wantToSell": wantToSell} for company in portfolio}
        # Get max sentiment among all companies
        min_sentiment = 2
        max_sentiment = -2
        max_company = None
        min_company = None
        for company in daily_data:
            if daily_data[company].Sentiment < min_sentiment:
                if daily_data[company].Volume > 40:
                    min_sentiment = daily_data[company].Sentiment
                    min_company = company
            elif daily_data[company].Sentiment > max_sentiment:
                if daily_data[company].Volume > 40:
                    max_sentiment = daily_data[company].Sentiment
                    max_company = company
        # Buy company with max sentiment
        if min_company is not None:
            new_portfolio[min_company]["shares"] -= np.floor(
                short_limit / daily_data[min_company].Close
            )
            new_portfolio[max_company]["wantToSell"] = False
        # Short company with min sentiment
        if max_company is not None:
            new_portfolio[max_company]["shares"] += np.floor(
                money / daily_data[max_company].Close
            )
            new_portfolio[max_company]["wantToSell"] = False
        return new_portfolio
