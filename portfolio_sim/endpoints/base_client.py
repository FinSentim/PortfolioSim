import pandas as pd

from abc import ABC, abstractmethod

class BaseAPI(ABC):

    """Super class for retrieving data from APIs"""
    def __init__(self):
        pass

    @abstractmethod
    def _get_company_data(self, comp_name):
        pass
    
    def get_company_data(self, comp_name, start_date=None, end_date=None):
        data = self._get_company_data(comp_name)
        data = self.post_process_data(data, start_date, end_date)
        return data
    
    
    def simulate_stock(self, companies,
                       start_date,
                       end_date):
        date_range = pd.date_range(start=start_date, end=end_date, freq="B")
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        companies_dict = {}
        for company in companies:
            df = self.get_company_data(company)
            df = df.loc[start_date:end_date]
            df = df[df.Close.notna()]
            companies_dict[company] = df
        company_data_dict = {}
        for date in date_range:
            day_stock_dict = {}
            for company in companies_dict:
                if date in companies_dict[company].index:
                    day_stock_dict[company] = companies_dict[company].loc[date]
            company_data_dict[date] = day_stock_dict
        return company_data_dict

    def load_index_data(self, start_date, end_date):
        buzz = self.get_company_data("BUZZ")
        fadtx = self.get_company_data("FADTX")
        mood = self.get_company_data("MOOD")
        ixic = self.get_company_data("^IXIC")
        GSPC = self.get_company_data("^GSPC")
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
    
    def post_process_data(self, df, start_date, end_date):
        df = self.date_filter(df, start_date, end_date)
        
        # Round the float columns to 4 decimal places
        float_cols = df.select_dtypes(include='float').columns
        df_new = df.copy()
        df_new.loc[:, float_cols] = df_new.loc[:, float_cols].round(4)  
        
        # more post processing here
        
        return df_new
    
    def date_filter(self, df, start_date=None, end_date=None):
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        start_date = start_date if start_date else df.index.min()
        end_date = end_date if end_date else df.index.max()
        
        filtered_df = df.loc[start_date:end_date]
        return filtered_df[::-1]
