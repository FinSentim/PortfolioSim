from unittest.mock import Mock, patch
import pytest
import requests
import pandas as pd
import numpy as np
import utils

# import portfolio_sim.local_utils as local_utils
import unittest


class DefaultWidgetSizeTestCase(unittest.TestCase):
    def test_default_widget_size(self):
        self.assertEqual("HELLO", "HELLO")


class GetCompanyDataTestCase(unittest.TestCase):
    @patch("portfolio_sim.utils.requests.post")
    def test_get_company_data_when_response_ok(mock_get):

    # httpclient -> mock

    
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
                    None,
                ],
            ],
            "daily_twitter_tweets_volume": [[], []],
            "daily_twitter_tweets_sentiment": [[], []],
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = stock_info
        res = utils.get_company_data("BUZZ")

        stock_info = pd.DataFrame(
            columns=["Sentiment", "Volume", "Close", "Split"],
            data=[[np.NaN, np.NaN, 23.520, 1]],
            index=pd.DatetimeIndex(["2021-03-04"]),
        )
        assert stock_info.equals(res)

    @patch("portfolio_sim.utils.requests.post")
    def test_get_company_data_when_response_bad(mock_get):
        mock_get.return_value.ok = False

        with pytest.raises(requests.exceptions.RequestException):
            utils.get_company_data("BUZZ")


if __name__ == "__main__":
    unittest.main()
