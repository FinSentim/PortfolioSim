from flask import Flask, jsonify, request
import pandas as pd
import random

api = Flask(__name__)


@api.route("/simulate-stock-v1", methods=["GET"])
def get_sim_data():
    start_date = request.args.get("dateFrom")
    end_date = request.args.get("dateTo")
    stock_data_str = request.args.getlist("stock")
    stock_strat = [x.split(":") for x in stock_data_str]
    stock_strat_dict = {x[0]: x[1].split(",") for x in stock_strat}
    date_list = pd.date_range(start=start_date, end=end_date)
    data = {}
    for stock, strategy_list in stock_strat_dict.items():
        strategy_dict = {}
        for strategy in strategy_list:
            strategy_data = [random.random() for _ in date_list]
            strategy_dict[strategy] = strategy_data
        data[stock] = strategy_dict
    response = {"data": data}
    return jsonify(response)


api.run(host="localhost", port=8080, threaded=True)
