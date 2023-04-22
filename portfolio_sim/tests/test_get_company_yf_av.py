import pandas as pd
import numpy as np
import unittest
from portfolio_sim.endpoints.api_clients import YFinanceAPI, AlphaVantageAPI


class GetVerifyDatasourceConnectionDataTestCase(unittest.TestCase):
    def test_yfinance_connection(self):

        # arrange
        expected = pd.DataFrame(
            columns=["Close", "Split", "Sentiment", "Volume"],
            data=[[130.5307, 0.0, np.NaN, np.NaN]],
            index=pd.DatetimeIndex(["2023-01-10"]),
        )

        # act
        resData = YFinanceAPI().get_company_data(
            comp_name="AAPL",
            start_date="2023-01-10",
            end_date="2023-01-10")

        exp = expected.loc[:, 'Close'].values[0]
        res = resData.loc[:, 'Close'].values[0]

        # assert
        self.assertEqual(exp, res)

    def test_AlphaVantage_connection(self):

        # arrange
        expected = pd.DataFrame(
            columns=["Close", "Split", "Sentiment", "Volume"],
            data=[[130.5312, 0.0, np.NaN, np.NaN]],
            index=pd.DatetimeIndex(["2023-01-10"]),
        )

        # act
        resData = AlphaVantageAPI().get_company_data(
            comp_name="AAPL",
            start_date="2023-01-10",
            end_date="2023-01-10")

        exp = expected.loc[:, 'Close'].values[0]
        res = resData.loc[:, 'Close'].values[0]

        # assert
        self.assertEqual(exp, res)


class GetVerifyAPIPeriods(unittest.TestCase):

    def test_yfinance_periods(self):

        # arrange
        exp = 3

        # act
        resData = YFinanceAPI().get_company_data(
            comp_name="AAPL",
            start_date="2023-01-08",
            end_date="2023-01-11")

        res = resData.loc[:, 'Close'].count()

        # assert
        self.assertEqual(exp, res)

    def test_AlphaVantage_periods(self):

        # arrange
        exp = 3

        # act
        resData = AlphaVantageAPI().get_company_data(
            comp_name="AAPL",
            start_date="2023-01-09",
            end_date="2023-01-11")

        res = resData.loc[:, 'Close'].count()

        # assert
        self.assertEqual(exp, res)


if __name__ == "__main__":
    unittest.main()
