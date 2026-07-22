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

Overview

The Stock Analysis Dashboard is a Python-based financial analysis tool that automatically collects stock market data and generates a professional PDF report. It helps investors, students, and financial analysts quickly understand a company's financial performance, stock trends, and recent news.

The example below shows the analysis report generated for Reliance Industries Ltd (RELIANCE.NS) using live financial data.

Dashboard Features
1. Company Information

The report starts with the company's basic information:

Company Name: Reliance Industries Ltd
Stock Symbol: RELIANCE.NS
Industry: Oil & Gas Refining & Marketing
Current Share Price: ₹1327.20
Report Generation Date & Time

This gives users an overview of the selected company.

2. Key Financial Ratios

The dashboard displays important financial metrics that help evaluate the company's financial health.

Metric	Meaning
Market Cap	Total market value of the company. Larger companies are generally more stable.
52-Week High	Highest stock price in the last 12 months.
52-Week Low	Lowest stock price in the last 12 months.
P/E Ratio (Trailing)	Shows how much investors are willing to pay for each ₹1 of earnings.
Forward P/E	Expected valuation based on future earnings.
P/B Ratio	Compares market price with book value.
P/S Ratio	Compares company value with revenue.
EPS (Earnings Per Share)	Profit earned per share. Higher EPS generally indicates better profitability.
Dividend Yield	Percentage of profit distributed to shareholders.
Gross Margin	Percentage of revenue remaining after production costs.
Operating Margin	Profit from core business operations.
Net Margin	Final profit after all expenses.
ROE (Return on Equity)	Measures how efficiently shareholder money is used.
ROA (Return on Assets)	Shows how efficiently company assets generate profit.
Current Ratio	Measures the company's ability to pay short-term liabilities.
Debt-to-Equity Ratio	Indicates how much debt the company uses compared to shareholders' equity.
Charts
📉 1-Year Stock Price Chart

This chart shows the stock's performance over the last year.

It includes:

Daily closing price
50-Day Moving Average
200-Day Moving Average

These moving averages help identify market trends:

Price above moving averages → Bullish trend
Price below moving averages → Bearish trend
📊 Revenue vs Net Income

This bar chart compares:

Annual Revenue
Annual Net Income

It helps users understand:

Business growth
Profitability
Financial consistency across multiple years

Higher revenue with increasing net income usually indicates a financially healthy company.

Recent News

The report also displays the latest news headlines related to the selected company.

Examples include:

Quarterly earnings
Business expansion
Market performance
Major investments
Industry updates

Including news helps users understand the reasons behind stock price movements.

Technologies Used
Python
yFinance – Live stock market data
Pandas – Data processing
Matplotlib – Data visualization
Feedparser – Financial news
ReportLab – PDF report generation
Workflow
User enters Stock Symbol
          │
          ▼
Fetch Market Data (Yahoo Finance)
          │
          ▼
Calculate Financial Ratios
          │
          ▼
Generate Charts
          │
          ▼
Fetch Latest Financial News
          │
          ▼
Create Professional PDF Report
Key Highlights
📈 Live stock market data
📊 Professional financial ratio analysis
📉 Moving average trend analysis
💰 Revenue and profit comparison
📰 Latest financial news integration
📄 Automatic PDF report generation
⚡ Easy-to-use command-line interface
Example Output

The generated report includes:

Company profile
Key financial ratios
1-year stock price chart
Revenue vs. Net Income chart
Latest news headlines
Professional PDF layout suitable for presentations and project demonstrations

This project demonstrates practical skills in Python, financial data analysis, data visualization, API integration, PDF report generation, and automation, making it a strong portfolio project for roles in Financial Analysis, Data Analysis, Business Analytics, and Python Development.
