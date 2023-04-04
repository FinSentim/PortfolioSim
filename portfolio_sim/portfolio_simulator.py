import pandas as pd
import numpy as np
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

    def simulate_strategy(self, strategy):
        port_hist = {}
        action_hist = {}
        price_column = "Close"
        money = 1000
        # Static $10 brokerage fee
        tradingFee = 10
        # Static 3% interest on shorts
        interest = 1.03 
        # Static 50% short limit of total portfolio
        short_limit = money * 0.5
        # Init empty portfolio
        portfolio = {company: 0 for company in self.portfolio_companies}

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
            # New money amount -> new short limit
            short_limit = money * 0.5

            portfolio = {company: 0 for company in portfolio}
            port_hist[date] = money
            # Make decision based on given strategy
            # Dictionary key: 'company' 
            portfolio_order = strategy.get_decision(
                daily_data, portfolio, money, short_limit
            )
            action_hist[date] = portfolio_order
            for company in portfolio_order:
                # Check if buy order
                if portfolio_order[company] > 0:
                    # Ensure there are enough funds for the order
                    if (money >= daily_data[company].Close * portfolio_order[company] + tradingFee):
                        portfolio[company] += portfolio_order[company]
                        cost = daily_data[company].Close * portfolio_order[company] + tradingFee
                        money -= cost
                        print("Bought {} {} shares for ${} each, total cost with fees: ${}".format(
                            portfolio_order[company], company, daily_data[company].Close, cost))
                    else:
                        # Order can't be completed
                        print(daily_data[company].Close, portfolio_order[company], money)
                        raise ValueError(
                            "Not enough money, purchase value (w/ fees) - {}, money - {}".format(
                                daily_data[company].Close * portfolio_order[company] + tradingFee, money,))
                
                # Check if short or sell order
                elif portfolio_order[company] < 0:
                    # To simplify arithmetics logic:
                    absTotalDailyStockValue = abs(daily_data[company].Close * portfolio_order[company])

                    # Sell 
                    # TODO: we will need a variable output from the strategy that controls shorting vs selling
                    # if (wantToSell):
                    if (portfolio[company] >= abs(portfolio_order[company])):
                        portfolio[company] -= abs(portfolio_order[company])
                        totalSellValue = absTotalDailyStockValue - tradingFee
                        money += totalSellValue
                        print("Sold {} {} shares for ${} each, total return after fees: ${}".format(
                            abs(portfolio_order[company]), company, daily_data[company].Close, totalSellValue))
                    else:
                        # Order can't be completed
                        raise ValueError(
                            "Not enough stocks to sell, sell amount - {}, stock amount - {}".format(
                                abs(portfolio_order[company]),
                                portfolio[company]))

                    # Short
                    # else:
                    #     # Ensure there are enough funds for the order
                    #     if (short_limit >= daily_data[company].Close * portfolio_order[company] * interest):
                    #         portfolio[company] += portfolio_order[company]
                    #         short_limit -= absTotalDailyStockValue
                    #         money -= absTotalDailyStockValue * interest + tradingFee
                    #     else:
                    #         # Order can't be completed
                    #         raise ValueError(
                    #             "Not enough short limit, short value (w/ fees/interest) - {}, short limit - {}".format(
                    #                 absTotalDailyStockValue * interest + tradingFee,
                    #                 short_limit,
                    #             )
                    #         )    
                
                # Strategy decided to hold position          
                else:
                    print("Hold position on {}".format(company))
                    
        # Finalize portfolio evaluation
        money += sum(
            [
                daily_data[company][price_column] * portfolio[company]
                for company in portfolio
            ]
        )
        portfolio = {company: 0 for company in portfolio}
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
