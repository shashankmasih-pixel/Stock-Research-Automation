# 📈 Stock Research Automation

Enter a stock ticker and get back a one-page equity research snapshot PDF.
The script automatically:

1. **Downloads financial data** – price history, company overview, income
   statement, and balance sheet, all via Yahoo Finance (`yfinance`).
2. **Calculates financial ratios** – valuation multiples (P/E, P/B, P/S),
   profitability (gross/net/operating margin, ROE, ROA), and liquidity /
   leverage (current ratio, debt-to-equity). Ratios are computed directly
   from the financial statements where possible, falling back to Yahoo's
   own snapshot fields if statement data isn't available for a ticker.
3. **Plots charts** – 1-year price chart with 50-day/200-day moving
   averages, and a revenue-vs-net-income bar chart from the last few
   fiscal years.
4. **Summarizes recent news** – pulls the latest headlines and short
   summaries from the Yahoo Finance RSS feed for the ticker (falls back to
   `yfinance`'s built-in news list if the feed is unavailable).
5. **Generates a one-page PDF report** – company header, ratio tables,
   charts, and news, laid out to fit on a single A4 page.

## Setup

```bash
pip install -r requirements.txt
```

No API keys needed — data comes from free Yahoo Finance endpoints.

## Running it

```bash
# single ticker
python stock_research_automation.py AAPL

# multiple tickers in one run
python stock_research_automation.py AAPL MSFT INFY.NS

# or run with no arguments and it will prompt you
python stock_research_automation.py
```

Reports are saved to `reports/<TICKER>_<timestamp>.pdf`.

Use the exchange suffix Yahoo Finance expects for non-US tickers, e.g.
`INFY.NS` (NSE), `RELIANCE.BO` (BSE), `HSBA.L` (LSE).

## Notes

- Data is free but unofficial and may be delayed — this is a research /
  portfolio tool, not a licensed data feed, and the report isn't investment
  advice.
- If a ticker has sparse fundamental data (common for some ETFs, indices,
  or newer listings), the ratio table will show `N/A` for anything that
  can't be computed rather than failing the whole report.
- To change how many news items are shown, edit `max_items` in the
  `fetch_news()` call inside `research_ticker()`.
- To add more ratios (e.g. quick ratio, interest coverage), extend
  `calculate_ratios()` — the `_get_row()` helper already handles pulling
  values out of the raw financial statements by row label.


<img width="1012" height="783" alt="image" src="https://github.com/user-attachments/assets/f714464a-47ed-46e1-9b10-59792dfd162c" />


## 📄 Report Overview

The **Stock Report Automation** project is a Python-based application that automatically generates a professional PDF stock analysis report using live market data from Yahoo Finance. It collects financial information, creates charts, fetches the latest news, and compiles everything into a well-formatted report.

### 📑 Report Contents

- **Company Information** – Company name, stock symbol, industry, current stock price, and report generation date.
- **Key Financial Ratios** – Market Cap, P/E Ratio, EPS, ROE, ROA, Current Ratio, Debt-to-Equity Ratio, and other important financial metrics.
- **Stock Price Analysis** – A 1-year stock price chart with 50-day and 200-day moving averages.
- **Financial Performance** – Annual Revenue vs. Net Income comparison chart.
- **Latest News** – Recent company-related financial news headlines.

### 🚀 Features

- Automatic PDF report generation
- Live stock market data
- Financial ratio analysis
- Stock price trend visualization
- Revenue vs. Net Income comparison
- Latest financial news integration

This project demonstrates skills in **Python, Financial Data Analysis, Data Visualization, API Integration, PDF Report Generation, and Automation**.

- Financial Analyst
- Business Analyst
- Data Analyst
- Investment Research Analyst
- Python Developer
