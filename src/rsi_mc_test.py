from helper_functions import fetch_stock_data, log_run
from stationary_permutation import get_permutation
import pandas as pd
import pandas_ta as ta
import numpy as np
import os
import click
from rsi_strategy import rsi_return
import sys
import logging


@click.command()
@click.option("-t", "--ticker", required=True, help="Stock Ticker (e.g., BTC-USD)")
@click.option("-s", "--start", default="2020-01-01", help="Start Date (YYYY-MM-DD)")
@click.option("-e", "--end", default="2023-12-31", help="End Date (YYYY-MM-DD)")
@click.option("--rsi-lookback", default=14, help="RSI Lookback value")
@click.option("--rsi-buy", default=30, help="RSI buy threshold")
@click.option("--rsi-sell", default=70, help="RSI sell threshold")
@click.option("--simulation-number", default=100, help="Number of random simulations")
@click.option("--output-file", required=True, help="Name of the output file")
@click.option("--strategy-name", default="RSI")
def main(
    ticker,
    start,
    end,
    rsi_lookback,
    rsi_buy,
    rsi_sell,
    output_file,
    strategy_name,
):
    log_run()
    try:
        stock_data = fetch_stock_data(ticker=ticker, start_date=start, end_date=end)
    except Exception as e:
        logging.error(f"Failed to fetch ticker {ticker}: {e}")
        sys.exit(1)

    log_strategy_return, log_return = rsi_return(
        ohlc=stock_data,
        rsi_lookback=rsi_lookback,
        buy_threshold=rsi_buy,
        sell_threshold=rsi_sell,
    )

    # B. The Final Total Number (Log Scale)
    total_log_return = log_strategy_return.iloc[-1]

    # C. The Real Percentage (Money in Wallet)
    # Formula: e^(log_return) - 1
    total_percent_return = np.exp(total_log_return) - 1
