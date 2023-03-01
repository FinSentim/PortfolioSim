import requests
import pandas as pd

from portfolio_sim import utils
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
    index_data = utils.FinsentimAPI().\
        load_index_data("2022-08-01", "2022-08-12")
    index_data = index_data.drop(columns=["MOOD", "BUZZ"])

    # Simulate Portfolio
    company_data_dict = utils.FinsentimAPI().\
        simulate_stock(comp_table, "2022-08-10", "2022-08-12")

    ps = PortfolioSimulator(
        company_data_dict,
        comp_table,
        MinMaxSentimentStrategy(),
        index_data,
    )
    ps.simulate_portfolio()
    print(ps.compare_baselines())
