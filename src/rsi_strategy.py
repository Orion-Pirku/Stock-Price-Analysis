#!/usr/bin/env python
import click
import numpy as np
import pandas as pd
import pandas_ta as ta
import logging
import sys
import matplotlib.pyplot as plt
import itertools
from helper_functions import fetch_stock_data, log_run


def rsi_return(
    ohlc: pd.DataFrame,
    rsi_lookback: int = 14,
    buy_threshold: int = 30,
    sell_threshold: int = 70,
) -> tuple[pd.Series, pd.Series]:
    df = ohlc.copy()
    df["RSI"] = ta.rsi(df["Close"], length=rsi_lookback)
    df["Signal"] = np.nan
    df.loc[df["RSI"] < buy_threshold, "Signal"] = 1
    df.loc[df["RSI"] > sell_threshold, "Signal"] = 0
    df["Position"] = df["Signal"].shift(1).ffill().fillna(0)
    log_returns = (df["Close"] / df["Close"].shift(1)).apply(np.log).dropna()
    strategy_returns = log_returns * df["Position"].shift(1)
    return strategy_returns.cumsum(), log_returns.cumsum()


def optimize_rsi(ohlc: pd.DataFrame):
    lookbacks = range(14, 100, 2)
    buy_threshold = range(20, 45, 5)
    sell_threshold = range(60, 85, 5)
    best_params = (14, 30, 70)
    best_return = 0.0

    combinations = itertools.product(lookbacks, buy_threshold, sell_threshold)
    for lookback, buy, sell in combinations:
        if buy >= sell:
            continue
        strategy_returns, _ = rsi_return(
            ohlc, rsi_lookback=lookback, buy_threshold=buy, sell_threshold=sell
        )
        avg_strategy_return = strategy_returns.mean()
        std_strategy_return = strategy_returns.std()

        if std_strategy_return == 0:
            sharpe = 0
        else:
            sharpe = (avg_strategy_return / std_strategy_return) * np.sqrt(365)
        if sharpe > best_return:
            best_return = sharpe
            best_params = (lookback, buy, sell)
    print(
        f"Optimization Complete. Best Sharpe: {best_return:.4f} | Params: {best_params}"
    )
    return best_params


def plot_strategy_comparison(
    log_return: pd.Series,
    log_strategy_return: pd.Series,
    ticker: str,
    strategy_name: str,
    output_file: str,
    figsize: tuple = (16, 10),
):
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Plot 1: Buy and hold
    ax1.plot(
        log_return.index,
        log_return,
        color="firebrick",
        label="Log Returns",
        linewidth=2,
    )
    ax1.set_title(ticker, fontsize=18)

    # Plot 2: Strategy
    ax2.plot(
        log_strategy_return.index,
        log_strategy_return,
        color="darkblue",
        label="Log Strategy Returns",
        linewidth=2,
    )
    ax2.set_title(strategy_name, fontsize=18)
    # Apply styling to both
    for ax in [ax1, ax2]:
        ax.set_xlabel("Date", fontsize=14)
        ax.set_ylabel("Log Return", fontsize=14)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper left", fontsize=12)

    plt.tight_layout()
    plt.savefig(output_file, dpi=200)


@click.command("StrategyReturn")
@click.option("-t", "--ticker", required=True, help="Stock Ticker (e.g., BTC-USD)")
@click.option("-s", "--start", default="2020-01-01", help="Start Date (YYYY-MM-DD)")
@click.option("-e", "--end", default="2023-12-31", help="End Date (YYYY-MM-DD)")
@click.option("--rsi-lookback", default=14, help="RSI Lookback value")
@click.option("--rsi-buy", default=30, help="RSI buy threshold")
@click.option("--rsi-sell", default=70, help="RSI sell threshold")
@click.option("--optimize", default=False)
@click.option("--output-file", required=True, help="Name of the output file")
@click.option("--strategy-name", default="RSI")
def main(
    ticker,
    start,
    end,
    rsi_lookback,
    rsi_buy,
    rsi_sell,
    optimize,
    output_file,
    strategy_name,
):
    log_run()
    try:
        stock_data = fetch_stock_data(ticker=ticker, start_date=start, end_date=end)
    except Exception as e:
        logging.error(f"Failed to fetch ticker {ticker}: {e}")
        sys.exit(1)
    if optimize:
        rsi_lookback, rsi_buy, rsi_sell = optimize_rsi(stock_data)

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

    # --- STEP 3: PRINT REPORT (Runs only once) ---
    print(f"\n" + "=" * 40)
    print(f" FINAL RESULTS FOR {ticker}")
    print(f"=" * 40)
    print(f"Strategy Params:      L:{rsi_lookback} | Buy:{rsi_buy} | Sell:{rsi_sell}")
    print(f"Total Log Return:     {total_log_return:.4f}")
    print(f"Total Profit/Loss:    {total_percent_return:.2%} (Real Value)")
    print(f"=" * 40 + "\n")

    plot_strategy_comparison(
        log_return, log_strategy_return, ticker, output_file, strategy_name
    )


if __name__ == "__main__":
    main()
