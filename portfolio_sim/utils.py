import pandas as pd
import requests
import urllib.parse


def get_company_data(comp_name):
    # comp_name = 'JP Morgan Chase & Co. Common Stock'
    url = "https://api.finsentim.com/latest/companies/data_dict/?key=jhcfkw0dfqe0gh8zw2eaun82yxggpevd%20&company={}".format(
        urllib.parse.quote(comp_name)
    )
    res = requests.post(
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
            f"Something went wrong with the request. Status code: {res.status_code}"
        )

    res = res.json()
    d_c = pd.DataFrame({"Close": res["daily_close"][1]}, index=res["daily_close"][0])
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
    df = d_t.merge(d_v, how="outer", left_index=True, right_index=True)
    df = df.merge(d_c, how="outer", left_index=True, right_index=True)
    df = df.merge(d_s, how="left", left_index=True, right_index=True)
    df.index = pd.DatetimeIndex(df.index)
    return df


def simulate_stock(
    companies,
    start_date,
    end_date,
):
    date_range = pd.date_range(start=start_date, end=end_date, freq="B")
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    companies_dict = {}
    for company in companies:
        df = get_company_data(company)
        df = df.loc[start_date:end_date]
        df = df[df.Close.notna()]
        companies_dict[company] = df
    company_data_dict = {}
    for date in date_range:
        day_stock_dict = {}
        for company in companies_dict:
            if date in companies_dict[company].index:
                # print(date, company, companies_dict[company].loc[date].Close)
                day_stock_dict[company] = companies_dict[company].loc[date]
        company_data_dict[date] = day_stock_dict
    return company_data_dict


def load_index_data(start_date, end_date):
    # buzz = pd.read_csv("data/BUZZ.csv")
    # fadtx = pd.read_csv("data/FADTX.csv")
    # mood = pd.read_csv("data/MOOD.csv")
    # ixic = pd.read_csv("data/^IXIC.csv")
    # GSPC = pd.read_csv("data/^GSPC.csv")
    buzz = get_company_data("BUZZ")
    fadtx = get_company_data("FADTX")
    mood = get_company_data("MOOD")
    ixic = get_company_data("^IXIC")
    GSPC = get_company_data("^GSPC")
    buzz.index = pd.to_datetime(buzz.index)
    fadtx.index = pd.to_datetime(fadtx.index)
    mood.index = pd.to_datetime(mood.index)
    ixic.index = pd.to_datetime(ixic.index)
    GSPC.index = pd.to_datetime(GSPC.index)
    all_indexes = pd.DataFrame(
        {
            "BUZZ": buzz.Close,
            "FADTX": fadtx.Close,
            "NASDAQ Composite (^IXIC)": ixic.Close,
            "S&P 500 (^GSPC)": GSPC.Close,
            "MOOD": mood.Close,
        }
    )
    return all_indexes.loc[start_date:end_date]
