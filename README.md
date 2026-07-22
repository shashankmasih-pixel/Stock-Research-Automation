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


# 📈 Stock Analysis Dashboard

A Python-based financial analysis tool that fetches live stock market data, performs financial analysis, generates charts, collects the latest company news, and automatically creates a professional PDF report.

---

## 📖 Overview

The **Stock Analysis Dashboard** helps investors, students, and financial analysts quickly understand a company's financial performance through an automatically generated report.

The dashboard uses **Yahoo Finance** to retrieve real-time financial information and presents it in an easy-to-read PDF format containing:

- Company Information
- Key Financial Ratios
- Stock Price Trend
- Revenue vs Net Income Comparison
- Latest Financial News

The example shown below is generated for **Reliance Industries Ltd (RELIANCE.NS)**.

---

# 📄 Dashboard Explanation

## 1. Company Information

At the top of the report, the dashboard displays the company's basic details.

It includes:

- Company Name
- Stock Symbol
- Industry
- Current Share Price
- Report Generation Date & Time

This section provides a quick overview of the selected company.

---

# 📊 Charts

## 1. One-Year Stock Price Trend

The first chart visualizes the stock's price movement over the past year.

It includes:

- Daily Closing Price
- 50-Day Moving Average
- 200-Day Moving Average

### Purpose

- Identify long-term market trends.
- Detect bullish or bearish momentum.
- Compare short-term and long-term price movements.

---

## 2. Revenue vs Net Income

This bar chart compares annual:

- Revenue
- Net Income

### Purpose

- Measure business growth.
- Compare sales with profitability.
- Evaluate financial consistency across multiple years.

A company with increasing revenue and growing net income generally indicates healthy financial performance.

---

# 📰 Recent News

The report automatically fetches the latest news headlines related to the selected company.

Examples include:

- Quarterly earnings
- Business expansion
- Market updates
- Investment announcements
- Industry developments

Including recent news helps users understand the events influencing stock price movements.

---

# ⚙️ Technologies Used

- Python
- yFinance
- Pandas
- Matplotlib
- Feedparser
- ReportLab

---

# 🔄 Project Workflow

```text
User enters Stock Symbol
        │
        ▼
Fetch Live Market Data
        │
        ▼
Extract Financial Ratios
        │
        ▼
Generate Stock Price Chart
        │
        ▼
Generate Revenue vs Net Income Chart
        │
        ▼
Fetch Latest News Headlines
        │
        ▼
Create Professional PDF Report
```

---

# ✨ Features

- 📈 Live stock market data
- 📊 Financial ratio analysis
- 📉 Moving average trend analysis
- 💰 Revenue and profit comparison
- 📰 Latest financial news integration
- 📄 Automatic PDF report generation
- ⚡ Fast and lightweight
- 💻 Easy-to-use command-line interface

---

# 🎯 Project Objectives

- Automate financial report generation.
- Provide a quick overview of company fundamentals.
- Visualize stock performance using charts.
- Help investors make informed decisions.
- Demonstrate Python skills in data analysis and automation.

---

# 📂 Sample Output

The generated report contains:

- Company Profile
- Financial Ratios
- One-Year Stock Price Chart
- Revenue vs Net Income Chart
- Latest News Headlines
- Professionally formatted PDF report

---

# 🚀 Future Improvements

- Interactive dashboard using Streamlit
- Technical indicators (RSI, MACD, Bollinger Bands)
- Candlestick charts
- Peer company comparison
- Portfolio tracking
- AI-powered stock insights
- Export reports in Excel and HTML formats
- Email report automation

---

# 📌 Conclusion

The **Stock Analysis Dashboard** is a complete financial reporting solution that combines live market data, financial metrics, data visualization, and news into a single automated PDF report.

This project demonstrates practical skills in:

- Python Programming
- Financial Data Analysis
- Data Visualization
- API Integration
- PDF Report Generation
- Automation

It is an excellent portfolio project for roles such as:

- Financial Analyst
- Business Analyst
- Data Analyst
- Investment Research Analyst
- Python Developer
