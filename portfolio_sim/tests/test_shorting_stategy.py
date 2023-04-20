from unittest.mock import Mock, patch
import pytest
import requests
import pandas as pd
import numpy as np
import unittest
from portfolio_sim.endpoints.api_clients import FinsentimAPI, YFinanceAPI


class GetShortingDataTestCase(unittest.TestCase):
    @patch("requests.post")
    def test_get_data_when_response_ok(self, mock_get):

        stock_info = {
            "daily_close": [
                [
                    "2021-03-04",
                ],
                [
                    23.52,
                ],
            ],
            "stock_splits": [
                [
                    "2021-03-04",
                ],
                [
                    23.51,
                ],
            ],
            "daily_twitter_tweets_volume": [[], []],
            "daily_twitter_tweets_sentiment": [[], []],
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = stock_info
        res = FinsentimAPI().get_company_data("BUZZ")

        stock_info = pd.DataFrame(
            columns=["Sentiment", "Volume", "Close", "Split"],
            data=[[np.NaN, np.NaN, 23.520, 1]],
            index=pd.DatetimeIndex(["2021-03-04"]),
        )
        assert stock_info.equals(res)

    @patch("requests.post")
    def test_get_company_data_when_response_bad(self, mock_get):
        mock_get.return_value.ok = False

        with pytest.raises(requests.exceptions.RequestException):
            FinsentimAPI().get_company_data("BUZZ")


class GEEEEETTTEEEEM(unittest.TestCase):
    @patch("yfinance.Ticker")
    def test_get_company_data(self, mock_get):

        mock_get.return_value.history.return_value = pd.DataFrame(
            columns=["Close", "Stock Splits"],
            data=[[23.52, 1]],
            index=pd.DatetimeIndex(["2021-03-04"]),
        )
        res = YFinanceAPI().get_company_data("BUZZ")
        stock_info = pd.DataFrame(
            columns=["Close", "Split", "Sentiment", "Volume"],
            data=[[23.520, 1, np.NaN, np.NaN]],
            index=pd.DatetimeIndex(["2021-03-04"]),
        )
        assert stock_info.equals(res)


if __name__ == "__main__":
    unittest.main()
