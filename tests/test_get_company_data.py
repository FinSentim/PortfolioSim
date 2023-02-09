from unittest.mock import Mock, patch
import pytest
import requests
import sys
import os
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'portfolio_sim'))
import local_utils


@patch('portfolio_sim.local_utils.requests.post')
def test_get_company_data_when_response_ok(mock_get):
    stock_info = {
            "daily_close": [
                [
                    "2021-03-04",
                ],
                [
                    23.52,
                ]],
            "stock_splits": [
                [
                    "2021-03-04",
                ],
                [
                    None,
                ]],
            "daily_twitter_tweets_volume": [
                [

                ],
                [

                ]],
            "daily_twitter_tweets_sentiment": [
                [

                ],
                [

                ]],
            }

    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = stock_info
    res = local_utils.get_company_data("BUZZ")

    stock_info = pd.DataFrame(
       columns=["Sentiment", "Volume", "Close", "Split"],
       data=[[np.NaN, np.NaN, 23.520, 1]],
       index=pd.DatetimeIndex(["2021-03-04"])
       )
    assert stock_info.equals(res)

@patch('portfolio_sim.local_utils.requests.post')
def test_get_company_data_when_response_bad(mock_get):
    mock_get.return_value.ok = False

    with pytest.raises(requests.exceptions.RequestException):
        local_utils.get_company_data("BUZZ")

