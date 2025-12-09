import os
import yfinance as yf
import logging
import uuid
import pandas as pd
from datetime import datetime, date


def log_run():
    job_id = str(uuid.uuid4())[:8]
    os.makedirs("logs", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"logs/log_{current_time}_{job_id}.txt"
    logging.basicConfig(
        level=logging.INFO,
        filename=log_filename,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def fetch_stock_data(
    ticker: str, start_date: date, end_date: date, output_dir: str | None = "."
):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    if output_dir is not None:
        data.to_csv(
            f"{output_dir}/{ticker}_data_{start_date}_{end_date}.csv",
            header=True,
            index=True,
        )
    return data
