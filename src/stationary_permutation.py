import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import ta


def _stationary_bootstrap_indices(
    n: int, p: float, rng: np.random.Generator
) -> np.ndarray:
    indices = np.zeros(n, dtype=int)
    current_idx = rng.integers(0, n)

    for i in range(n):
        if rng.random() < p:
            current_idx = rng.integers(0, n)
        else:
            current_idx = (current_idx + 1) % n
        indices[i] = current_idx
    return indices


def _decompose_data(
    ohlc: pd.DataFrame, start_index: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    df = ohlc.copy()
    df.columns = df.columns.str.lower()

    log_bars = df[["open", "high", "low", "close"]].apply(np.log)

    r_o = (log_bars["open"] - log_bars["close"].shift()).to_numpy()

    r_h = (log_bars["high"] - log_bars["open"]).to_numpy()
    r_l = (log_bars["low"] - log_bars["open"]).to_numpy()
    r_c = (log_bars["close"] - log_bars["open"]).to_numpy()

    perm_index = start_index + 1

    history_arr = log_bars.iloc[:perm_index].to_numpy()

    pool_o = r_o[perm_index:]
    pool_h = r_h[perm_index:]
    pool_l = r_l[perm_index:]
    pool_c = r_c[perm_index:]

    return history_arr, pool_o, pool_h, pool_l, pool_c


def _reconstruct_data(
    history_arr: np.ndarray,
    shuffled_o: np.ndarray,
    shuffled_h: np.ndarray,
    shuffled_l: np.ndarray,
    shuffled_c: np.ndarray,
    n_total: int,
) -> np.ndarray:
    output = np.zeros((n_total, 4))
    perm_index = len(history_arr)

    output[:perm_index] = history_arr

    for i in range(perm_index, n_total):
        k = i - perm_index

        output[i, 0] = output[i - 1, 3] + shuffled_o[k]
        output[i, 1] = output[i, 0] + shuffled_h[k]
        output[i, 2] = output[i, 0] + shuffled_l[k]
        output[i, 3] = output[i, 0] + shuffled_c[k]

    return np.exp(output)


def get_permutation(
    ohlc: pd.DataFrame, probability: float = 0.1, start_index: int = 0, seed=None
) -> pd.DataFrame:
    assert start_index >= 0
    rng = np.random.default_rng(seed)

    history, pool_o, pool_h, pool_l, pool_c = _decompose_data(ohlc, start_index)

    perm_n = len(pool_o)

    idx_intraday = _stationary_bootstrap_indices(perm_n, probability, rng)
    shuffled_h = pool_h[idx_intraday]
    shuffled_l = pool_l[idx_intraday]
    shuffled_c = pool_c[idx_intraday]

    idx_gap = _stationary_bootstrap_indices(perm_n, probability, rng)
    shuffled_o = pool_o[idx_gap]

    final_data = _reconstruct_data(
        history, shuffled_o, shuffled_h, shuffled_l, shuffled_c, len(ohlc)
    )

    return pd.DataFrame(
        final_data, index=ohlc.index, columns=["Open", "High", "Low", "Close"]
    )
