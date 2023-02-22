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

    pip install requests pandas

Running the simulation
----------------------

To run the simulation, you will need to provide a list of the companies in the portfolio and a time period for the simulation. You will also need to choose one or more strategies for deciding when to buy or sell the stocks.

Example programs can be found under 
    
    portfolio_sim/examples


Available Strategies
-------------------

The following strategies are available for use in the simulation:

-   `MaxSentimentLongStrategy`: buy stocks when sentiment is high and sell when sentiment is low
-   `MinSentimentShortStrategy`: sell stocks when sentiment is low and buy when sentiment is high
-   `MinMaxSentimentStrategy`: buy stocks when sentiment is high and sell when sentiment is low, but also sell stocks when sentiment is very low
-   `PropMaxSentimentLongStrategy`: buy stocks when sentiment is high and sell when sentiment is low, but also buy more stocks when sentiment is very high
-   `PropMinSentimentShortStrategy`: sell stocks when sentiment is low and buy when sentiment is high, but also sell more stocks when sentiment is very low
-   `PropMinMaxSentimentStrategy`: buy stocks when sentiment is high and sell when sentiment is low, but also sell more stocks when sentiment is very low and buy more stocks when sentiment is very high


Plotting Results
----------------

The simulation results can be plotted using either matplotlib or plotly. To use matplotlib, call the `plot_results` method with 
    `backend="matplotlib"`
