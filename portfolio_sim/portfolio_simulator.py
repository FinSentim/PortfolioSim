import pandas as pd
import numpy as np
from enum import Enum
#import matplotlib.pyplot as plt


class PortfolioSimulator:
    def __init__(
        self,
        simulation_data: dict,
        portfolio_companies: list,
        strategies: list,
        baselines=None,
    ) -> None:
        self.simulation_data = simulation_data
        self.portfolio_companies = portfolio_companies
        # Init dictionary to store performance
        self.port_hist_dict = {}
        self.baselines = baselines
        # Ensure strategies are given as a list
        if type(strategies) is list:
            self.strategies = strategies
        else:
            self.strategies = [strategies]

    # Strategy format: 
        # daily_data: pd.DataFrame,
        # portfolio: dict
        # money: float
        # short_limit: float
        # wantToSell: bool
    # daily_data, portfolio, money, short_limit, sell
    def simulate_strategy(self, strategy):
        port_hist = {}
        action_hist = {}
        price_column = "Close"
        money = 1000
        wantToSell = False
        # Static $10 brokerage fee
        tradingFee = 10
        # Static 3% interest on shorts
        interest = 1.03
        # Static 50% short limit of total portfolio
        short_limit = money * 0.5
        # Init empty portfolio
        portfolio = {company: 0 for company in self.portfolio_companies}
        short_positions = {company: (0, 0) for company in self.portfolio_companies}

        # Iterate through all days in the simulation
        for date in self.simulation_data.keys():
            daily_data = self.simulation_data[date]
            if not daily_data:
                continue
            # Evaluate portfolio
            money += sum(
                [
                    # Share price * amount of shares 
                    daily_data[company][price_column] * portfolio[company]
                    for company in portfolio
                ]
            )

            port_hist[date] = money
            # Make decision based on given strategy
            # Dictionary key: 'company' 
            portfolio_order = strategy.get_decision(
                daily_data, portfolio, money, short_limit, wantToSell
            )
            action_hist[date] = portfolio_order

            # Keep in mind: difference between changing portfolio and cost/sell price
            # portfolio = number of shares
            # cost/sell price = shares * stock price
            for company in portfolio_order:
                # Number of shares to change the portfolio by
                currentOrder = portfolio_order[company]["order"]
                # Check if buy order
                if currentOrder > 0:
                    # BUY

                    # Ensure there are enough funds for the order
                    if (money >= daily_data[company].Close * currentOrder + tradingFee):
                        portfolio[company] += currentOrder
                        cost = daily_data[company].Close * currentOrder + tradingFee
                        money -= cost
                        print("Bought {} {} shares for ${} each, total cost with fees: ${}".format(
                            currentOrder, company, daily_data[company].Close, cost))
                    else:
                        # Order can't be completed
                        print(daily_data[company].Close, currentOrder, money)
                        raise ValueError(
                            "Not enough money, purchase value (w/ fees) - {}, money - {}".format(
                                daily_data[company].Close * currentOrder + tradingFee, money,))
                
                # Check if short or sell order
                elif currentOrder < 0:
                    # To simplify arithmetics logic:
                    absTotalDailyStockValue = abs(daily_data[company].Close * currentOrder)

                    if (wantToSell):
                        # SELL
                        
                        # Ensure these are enough owned shares to complete the sell order 
                        if (portfolio[company] >= abs(currentOrder)):
                            portfolio[company] -= abs(currentOrder)
                            totalSellValue = absTotalDailyStockValue - tradingFee
                            money += totalSellValue
                            print("Sold {} {} shares for ${} each, total return after fees: ${}".format(
                                abs(currentOrder), company, daily_data[company].Close, totalSellValue))
                        else:
                            # Order can't be completed
                            raise ValueError(
                                "Not enough stocks to sell, sell amount - {}, stock amount - {}".format(
                                    abs(currentOrder),
                                    portfolio[company]))
                    else:
                        # SHORT

                        # TODO: Currently shorts are not able to be closed,
                        #       this is due to no strategy ever closes it.

                        # Ensure there is enough short_limit for the order
                        # Short_limit < money, since short_limit is 50% of money
                        if (short_limit >= daily_data[company].Close * currentOrder * interest):
                            portfolio[company] += currentOrder
                            # Update short_positions with order size and the day's stock price
                            # This is required since the result of the short is based on entry price
                            short_positions[company] = (currentOrder, daily_data[company].Close)
                            short_limit -= absTotalDailyStockValue
                            money -= absTotalDailyStockValue * interest + tradingFee
                            print("Shorted {} {} shares for ${} each, total cost with fees and interest: ${}".format(
                                abs(currentOrder), company, daily_data[company].Close, absTotalDailyStockValue * interest + tradingFee))
                        else:
                            # Order can't be completed
                            raise ValueError(
                                "Not enough short limit, short value (w/ fees/interest) - {}, short limit - {}".format(
                                    absTotalDailyStockValue * interest + tradingFee,
                                    short_limit,
                                )
                            )
                
                # Strategy decided to hold position          
                else:
                    print("Hold current position on {}".format(company))

                # New money amount -> new short limit
                short_limit = money * 0.5
                    
        # Finalize portfolio evaluation
        money += sum(
            [
                daily_data[company][price_column] * portfolio[company]
                for company in portfolio
            ]
        )
        portfolio = {company: {"order": 0, "wantToSell": wantToSell} for company in portfolio}
        port_hist[date] = money
        self.port_hist_dict[strategy.name] = pd.Series(port_hist, name=strategy.name)
        # self.action_hist = pd.DataFrame(action_hist)

    def simulate_portfolio(self):
            # Iterate through all strategies and simulate each one
        for strategy in self.strategies:
            self.simulate_strategy(strategy)
        # Create a DataFrame containing the portfolio history for each strategy
        self.results_df = pd.DataFrame(self.port_hist_dict)

    def compare_baselines(self, cat="None"):
        if self.baselines is None:
            return None
        # Merge baseline data with the results DataFrame
        self.comparison_res = self.baselines.merge(
            self.results_df,
            left_index=True,
            right_index=True,
            how="right",
        )
        # Normalize the comparison data by dividing by the first row
        self.comparison_res = self.comparison_res / self.comparison_res.iloc[0]
        return self.comparison_res

    def plot_results(self, backend="matplotlib"):
        if backend == "matplotlib":
            pd.options.plotting.backend = "matplotlib"
            return self.compare_baselines().plot(figsize=(10, 5))
        elif backend == "plotly":
            pd.options.plotting.backend = "plotly"
            return self.comparison_res.plot()
        
