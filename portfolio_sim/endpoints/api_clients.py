import pandas as pd
import requests
import urllib.parse
import yfinance as yf
import numpy as np

from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from base_client import BaseAPI


class FinsentimAPI(BaseAPI):
    """Class for retrieving data from Finsentim API"""
    def __init__(self):
        self.session = CachedLimiterSession(
            per_second=0.9,
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("finsentim.cache"),
        )

    # get_company_data implementation for Finsentim API
    def _get_company_data(self, comp_name):
        # format the url request with the api key
        url = """https://api.finsentim.com/latest/
                 companies/data_dict/
                 ?key=jhcfkw0dfqe0gh8zw2eaun82yxggpevd%20&
                 company={}""".format(
                    urllib.parse.quote(comp_name)
                )
        # make the request, store it using self.session
        res = self.session.post(
            url,
            json={
                "requested_sources": [
                    "daily_close",
                    "stock_splits",
                    "daily_twitter_tweets_volume",
                    "daily_twitter_tweets_sentiment",
                ]
            },
        )
        # Check if response is valid
        if not res.ok:
            raise requests.exceptions.RequestException(
                f"""Something went wrong
                    with the request.
                    Status code: {res.status_code}"""
            )
            
        # the returned response to json
        res = res.json()

        # create a dataframe for each data type
        d_c = pd.DataFrame({"Close": res["daily_close"][1]},
                           index=res["daily_close"][0])


        d_s = pd.DataFrame(
            {"Split": res["stock_splits"][1]}, index=res["stock_splits"][0]
        ).fillna(1)

        d_v = pd.DataFrame(
            {"Volume": res["daily_twitter_tweets_volume"][1]},
            index=res["daily_twitter_tweets_volume"][0],
        )

        d_t = pd.DataFrame(
            {"Sentiment": res["daily_twitter_tweets_sentiment"][1]},
            index=res["daily_twitter_tweets_sentiment"][0],
        )
        
        # merge the dataframes
        df = d_t.merge(d_v, how="outer", left_index=True, right_index=True)
        df = df.merge(d_c, how="outer", left_index=True, right_index=True)
        df = df.merge(d_s, how="left", left_index=True, right_index=True)
        df.index = pd.DatetimeIndex(df.index)
        return df


class CachedLimiterSession(CacheMixin, LimiterMixin, requests.Session):
    """A class for caching and limiting requests"""
    
class YFinanceAPI(BaseAPI):
    """Class for retrieving data from YFinance API"""
    def __init__(self):
        self.session = CachedLimiterSession(
            per_second=0.9,
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("yfinance.cache"),
        )
        return

    def _get_company_data(self, comp_name):
        # TODO (Tim):
        # Only retrieve the time period we need from the API
        # Implementable when we have all three data sources in place.
        df = yf.Ticker(comp_name, session=self.session).\
            history(period="max",
                    actions=True,
                    raise_errors=True,
                    debug=True)

        df2 = df[['Close', 'Stock Splits']]
        df2 = df2.rename(columns={'Close': 'Close', 'Stock Splits': 'Split'})
        df2["Sentiment"] = np.NaN
        df2["Volume"] = np.NaN
        df2.index = pd.DatetimeIndex(df2.index)
        return df2
    

class AlphaVantageAPI(BaseAPI):
    """Class for retrieving data from AlphaVantage API"""
    
    # set the api key and session cache
    def __init__(self):
        self.session = CachedLimiterSession(
            per_second=0.9,
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("alphavantage.cache"),
        )
        self.api_key = "H1ATKVP3UMENMSPG"
    
    
    def _get_company_data(self, comp_name):
        
        # Get daily close and stock splits data
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={comp_name}&apikey={self.api_key}&datatype=json&outputsize=full"
        
        # get the response, store it using self.session
        res = self.session.get(url)
        
        # if an error occured, raise an exception
        if not res.ok:
            raise requests.exceptions.RequestException(
                f"Something went wrong with the request. Status code: {res.status_code}"
            )
            
        # the returned response to json
        res = res.json()

        # create a dataframe for each data type
        df = pd.DataFrame(
            {
                # insert close data from alphavantage
                "Close": [
                    float(res["Time Series (Daily)"][date]["5. adjusted close"])
                    for date in res["Time Series (Daily)"]
                ],
                # insert split data from alphavantage
                "Split": [
                    res["Time Series (Daily)"][date]["8. split coefficient"]
                    for date in res["Time Series (Daily)"]
                ],
            },
            index=[date for date in res["Time Series (Daily)"]],
        )
        
        # set these to null
        df["Sentiment"] = np.NaN
        df["Volume"] = np.NaN
        df.index = pd.DatetimeIndex(df.index)
        df.index.name = "Date"

        return df
    
"""

Run:
<api_class>.get_company_data(<ticker>)

Ex: 
AlphaVantageAPI().get_company_data("MSFT") retreives data for Microsoft from AlphaVantage

AlphaVantageAPI().get_company_data("MSFT", "2002-10-09", "2009-02-24") retreives data for Microsoft from AlphaVantage between the dates 2002-10-09 and 2009-02-24

AlphaVantageAPI().get_company_data("MSFT", end_date="2002-10-09") retreives data for Microsoft from AlphaVantage until the date 2002-10-09

AlphaVantageAPI().get_company_data("MSFT", "2002-10-09") retreives data for Microsoft from AlphaVantage from the date 2002-10-09 until today

"""