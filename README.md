# Stock Price Monte Carlo Simulation

A Python-based tool for estimating future stock price paths using Monte Carlo simulations. This project analyzes historical stock data, calculates logarithmic returns, and uses statistical modeling to generate potential future price scenarios.

## 📊 Overview

This repository contains proprietary scripts to:
1.  **Ingest** historical stock price data.
2.  **Analyze** historical volatility and drift using Logarithmic Returns.
3.  **Simulate** thousands of potential future price paths using Geometric Brownian Motion (GBM).
4.  **Visualize** the distribution of potential outcomes and confidence intervals.

## 🛠️ Technologies & Dependencies

All external Python packages and libraries required to run this project are listed in `requirements.txt`.

The project utilizes standard open-source libraries for:
* Data Manipulation & Analysis
* Visualization
* Machine Learning & Econometrics (ARCH/GARCH)
* Statistical Modeling

## ⚙️ Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Orion-Pirku/Stock-Price-Analysis.git
    ```

2.  Install the required packages from the requirements file:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

1.  **Load Data:** The script initializes by cleaning missing data and calculating daily Log Returns:
    $$ \text{Log Return} = \ln\left(\frac{P_t}{P_{t-1}}\right) $$

2.  **Run Simulation:**
    Run the main script to generate the simulations.
    ```python
    python main.py
    ```

3.  **Visualization:**
    The output will generate plots showing:
    * Histogram of historical Log Returns (Distribution analysis).
    * Line chart of multiple simulated future price paths.
    * Distribution of final predicted prices.

## 📈 Methodology

The simulation assumes that stock prices follow a **Geometric Brownian Motion (GBM)**, modeled as:

$$ dS_t = \mu S_t dt + \sigma S_t dW_t $$

Where:
* $S_t$ is the stock price.
* $\mu$ (drift) is the expected return.
* $\sigma$ (volatility) is the standard deviation of returns.
* $dW_t$ is a Wiener process (Brownian motion).

## ⚠️ Disclaimer

**Not Financial Advice.**
The content, code, and simulations in this repository are for educational and informational purposes only. They do not constitute financial advice, and you should not rely on them for investment decisions. Monte Carlo simulations are probabilistic models based on historical data, which is not a guarantee of future performance.

## © Copyright & License

**Copyright (c) 2025 Orion Pirku. All Rights Reserved.**

**Proprietary Source Code:**
The source code, logic, and implementation details contained within this repository are the exclusive property of Orion Pirku. This code is strictly for private use. Unauthorized copying, modification, distribution, or use of this file, via any medium, is strictly prohibited.

**Open Source Acknowledgement:**
This software makes use of open-source packages listed in `requirements.txt`. The rights to those specific libraries remain with their respective authors and are governed by their respective licenses (e.g., BSD, Apache, PSF). Use of these libraries in this project is in compliance with their permissive licensing terms.