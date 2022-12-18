Portfolio Simulator
-------------------

This project contains a tool for simulating the performance of a portfolio of stocks over a given time period. The tool uses historical data for the stocks and various strategies to make decisions about buying and selling the stocks.

Getting Started
===============

Prerequisites
-------------

This project requires the following packages:

- requests
- pandas

You can install these packages using `pip`:

::

    pip install requests pandas

Running the simulation
----------------------

To run the simulation, you will need to provide a list of the companies in the portfolio and a time period for the simulation. You will also need to choose one or more strategies for deciding when to buy or sell the stocks.

Here is an example of how you might run the simulation:

::

    import requests
    import pandas as pd

    from portfolio_sim.local_utils import simulate_stock, load_index_data
    from portfolio_sim.portfolio_simulator import PortfolioSimulator
    from portfolio_sim.strategies.single_strategies import MinMaxSentimentStrategy

    if __name__ == "__main__":
        ## Load Company list
        url = "https://api.finsentim.com/latest/companies/table/?key=jhcfkw0dfqe0gh8zw2eaun82yxggpevd%20"
        comp_table = requests.get(url)
        comp_table = pd.read_json(comp_table.json()).name

        ## Load Index Data
        index_data = load_index_data("2021-01-04", "2022-08-12")
        index_data = index_data.drop(columns=["MOOD", "BUZZ"])

        ## Simulate Portfolio
        company_data_dict = simulate_stock(comp_table, "2021-01-04", "2022-08-12")
        ps = PortfolioSimulator(
            company_data_dict,
            comp_table,
            MinMaxSentimentStrategy(),
            index_data,
        )
        ps.simulate_portfolio()
        print(ps.compare_baselines())

Available Strategies
-------------------

The following strategies are available for use in the simulation:

- `MaxSentimentLongStrategy`: buy stocks when sentiment is high
