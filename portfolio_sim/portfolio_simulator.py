import pandas as pd


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
        self.port_hist_dict = {}
        self.baselines = baselines
        if type(strategies) is list:
            self.strategies = strategies
        else:
            self.strategies = [strategies]

    def simulate_strategy(self, strategy):
        port_hist = {}
        action_hist = {}
        price_column = "Close"
        money = 1000
        short_limit = money * 0.5
        portfolio = {copmany: 0 for copmany in self.portfolio_companies}
        for date in self.simulation_data.keys():
            daily_data = self.simulation_data[date]
            if not daily_data:
                continue
            # Evaluate portfolio
            money += sum(
                [
                    daily_data[company][price_column] * portfolio[company]
                    for company in portfolio
                ]
            )
            short_limit = money * 0.5

            portfolio = {company: 0 for company in portfolio}
            port_hist[date] = money
            # Make decision
            portfolio_order = strategy.get_decision(
                daily_data, portfolio, money, short_limit
            )
            action_hist[date] = portfolio_order
            for company in portfolio_order:
                if portfolio_order[company] > 0:
                    if money >= daily_data[company].Close * portfolio_order[
                            company]:
                        portfolio[company] += portfolio_order[company]
                        money -= daily_data[company].Close * portfolio_order[
                            company]
                    else:
                        print(
                            daily_data[company].Close,
                            portfolio_order[company],
                            money
                        )
                        raise ValueError(
                            "Not enough money, purchase value - {}, money - {}"
                            .format(
                                daily_data[company].Close * portfolio_order[
                                    company],
                                money,
                            )
                        )
                elif portfolio_order[company] < 0:
                    if (
                        short_limit
                        >= daily_data[company].Close * portfolio_order[company]
                    ):
                        portfolio[company] += portfolio_order[company]
                        short_limit -= (
                            daily_data[company].Close * portfolio_order[
                                company]
                        )
                        money -= daily_data[company].Close * portfolio_order[
                            company]
                    else:
                        raise ValueError("Not enough short limit")

        money += sum(
            [
                daily_data[company][price_column] * portfolio[company]
                for company in portfolio
            ]
        )
        portfolio = {company: 0 for company in portfolio}
        port_hist[date] = money
        self.port_hist_dict[strategy.name] = pd.Series(
            port_hist,
            name=strategy.name)
        # self.action_hist = pd.DataFrame(action_hist)

    def simulate_portfolio(self):
        for strategy in self.strategies:
            self.simulate_strategy(strategy)
        self.results_df = pd.DataFrame(self.port_hist_dict)

    def compare_baselines(self, cat="None"):
        if self.baselines is None:
            return None
        self.comparison_res = self.baselines.merge(
            self.results_df,
            left_index=True,
            right_index=True,
            how="right",
        )
        self.comparison_res = self.comparison_res / self.comparison_res.iloc[0]
        return self.comparison_res

    def plot_results(self, backend="matplotlib"):
        if backend == "matplotlib":
            pd.options.plotting.backend = "matplotlib"
            return self.compare_baselines().plot(figsize=(10, 5))
        elif backend == "plotly":
            pd.options.plotting.backend = "plotly"
            return self.comparison_res.plot()
