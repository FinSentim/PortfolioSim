import requests
import pandas as pd

from portfolio_sim.endpoints.api_clients import FinsentimAPI
from portfolio_sim.portfolio_simulator import PortfolioSimulator
from portfolio_sim.strategies.single_strategies import MinMaxSentimentStrategy

if __name__ == "__main__":
    # Load Company list
    url = (
        "https://api.finsentim.com/latest/companies/"
        "table/?key=jhcfkw0dfqe0gh8zw2eaun82yxggpevd%20"
    )
    comp_table = requests.get(url)
    comp_table = pd.read_json(comp_table.json()).name

    # Load Index Data
    index_data = FinsentimAPI().\
        load_index_data("2022-08-01", "2022-08-12")
    index_data = index_data.drop(columns=["MOOD", "BUZZ"])

    apple = comp_table.loc[[1]]
    company_data_dict = FinsentimAPI().\
        simulate_stock(apple, "2022-08-01", "2022-08-12")

    # Simulate Portfolio
    ps = PortfolioSimulator(
        company_data_dict,
        apple,
        MinMaxSentimentStrategy(),
        index_data,
    )
    ps.simulate_portfolio()
    print(ps.compare_baselines())
