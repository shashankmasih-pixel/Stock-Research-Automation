"""
==================================================================
 STOCK RESEARCH AUTOMATION
==================================================================
Enter a stock ticker. The script automatically:

    1. Downloads financial data     (fetch_stock_data)
    2. Calculates financial ratios  (calculate_ratios)
    3. Plots charts                 (generate_charts)
    4. Summarizes recent news       (fetch_news)
    5. Generates a one-page PDF     (build_one_page_report)

Usage
-----
    python stock_research_automation.py AAPL
    python stock_research_automation.py          # will prompt for a ticker
    python stock_research_automation.py AAPL MSFT INFY.NS   # batch mode

Output
------
    reports/<TICKER>_<date>.pdf

Dependencies
------------
    pip install -r requirements.txt

Notes
-----
Data comes from Yahoo Finance via the `yfinance` library and is free but
unofficial/delayed - not a substitute for a licensed data feed or
professional research. This is a portfolio / educational tool, not
investment advice.

Author: Shashank Masih Toppo (portfolio project)
==================================================================
"""

import sys
import logging
import textwrap
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import yfinance as yf
import feedparser

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
)

REPORTS_FOLDER = Path("./reports")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
log = logging.getLogger("stock_research")


# ==================================================================
# 1. DATA DOWNLOAD
# ==================================================================
def fetch_stock_data(ticker: str) -> dict:
    """
    Pull everything needed for the report from Yahoo Finance:
      - info: company overview / valuation snapshot
      - history: 1 year of daily OHLCV price data
      - financials / balance_sheet: annual statements (for ratios)
    """
    log.info("Downloading data for %s ...", ticker)
    t = yf.Ticker(ticker)

    info = t.info or {}
    if not info or info.get("regularMarketPrice") is None and info.get("currentPrice") is None:
        # Some tickers still return a sparse info dict even when valid;
        # only hard-fail if there's truly nothing usable.
        if not info:
            raise ValueError(f"No data found for ticker '{ticker}'. Check the symbol and try again.")

    history = t.history(period="1y", interval="1d")
    if history.empty:
        raise ValueError(f"No price history found for ticker '{ticker}'.")

    try:
        financials = t.financials  # annual income statement
    except Exception:
        financials = pd.DataFrame()

    try:
        balance_sheet = t.balance_sheet
    except Exception:
        balance_sheet = pd.DataFrame()

    return {
        "ticker": ticker.upper(),
        "info": info,
        "history": history,
        "financials": financials,
        "balance_sheet": balance_sheet,
    }


# ==================================================================
# 2. FINANCIAL RATIOS
# ==================================================================
def _get_row(df: pd.DataFrame, candidates: list):
    """Return the most recent value of the first matching row label found."""
    if df is None or df.empty:
        return None
    for name in candidates:
        if name in df.index:
            series = df.loc[name].dropna()
            if len(series) > 0:
                return series.iloc[0]
    return None


def _safe_div(a, b):
    try:
        if a is None or b is None or b == 0:
            return None
        return a / b
    except (TypeError, ZeroDivisionError):
        return None


def calculate_ratios(data: dict) -> dict:
    """
    Compute a standard equity-research ratio set. Valuation multiples come
    from Yahoo's live snapshot (`info`); profitability/leverage ratios are
    computed directly from the financial statements where available, with
    `info` fields used as a fallback if statement data is missing.
    """
    info = data["info"]
    fin = data["financials"]
    bs = data["balance_sheet"]

    revenue = _get_row(fin, ["Total Revenue", "TotalRevenue"])
    gross_profit = _get_row(fin, ["Gross Profit", "GrossProfit"])
    net_income = _get_row(fin, ["Net Income", "NetIncome", "Net Income Common Stockholders"])
    operating_income = _get_row(fin, ["Operating Income", "OperatingIncome"])

    current_assets = _get_row(bs, ["Total Current Assets", "Current Assets"])
    current_liabilities = _get_row(bs, ["Total Current Liabilities", "Current Liabilities"])
    total_debt = _get_row(bs, ["Total Debt", "Total Liabilities Net Minority Interest"])
    total_equity = _get_row(bs, ["Total Equity Gross Minority Interest", "Stockholders Equity",
                                  "Total Stockholder Equity"])
    total_assets = _get_row(bs, ["Total Assets"])

    ratios = {
        "Company": info.get("shortName") or info.get("longName") or data["ticker"],
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Current Price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "Currency": info.get("currency", ""),
        "Market Cap": info.get("marketCap"),
        "52-Week High": info.get("fiftyTwoWeekHigh"),
        "52-Week Low": info.get("fiftyTwoWeekLow"),
        "Beta": info.get("beta"),

        # Valuation multiples (from Yahoo snapshot)
        "P/E (Trailing)": info.get("trailingPE"),
        "P/E (Forward)": info.get("forwardPE"),
        "P/B Ratio": info.get("priceToBook"),
        "P/S Ratio": info.get("priceToSalesTrailing12Months"),
        "EPS (Trailing)": info.get("trailingEps"),
        "Dividend Yield %": (info.get("dividendYield") * 100) if info.get("dividendYield") else None,

        # Profitability - computed from statements, fallback to info
        "Gross Margin %": (_safe_div(gross_profit, revenue) or info.get("grossMargins") or 0) * 100
            if (gross_profit is not None and revenue) or info.get("grossMargins") else None,
        "Net Margin %": (_safe_div(net_income, revenue) or info.get("profitMargins") or 0) * 100
            if (net_income is not None and revenue) or info.get("profitMargins") else None,
        "Operating Margin %": (_safe_div(operating_income, revenue) or info.get("operatingMargins") or 0) * 100
            if (operating_income is not None and revenue) or info.get("operatingMargins") else None,
        "ROE %": (_safe_div(net_income, total_equity) or info.get("returnOnEquity") or 0) * 100
            if (net_income is not None and total_equity) or info.get("returnOnEquity") else None,
        "ROA %": (_safe_div(net_income, total_assets) or info.get("returnOnAssets") or 0) * 100
            if (net_income is not None and total_assets) or info.get("returnOnAssets") else None,

        # Liquidity / leverage - computed from statements, fallback to info
        "Current Ratio": _safe_div(current_assets, current_liabilities) or info.get("currentRatio"),
        "Debt-to-Equity": _safe_div(total_debt, total_equity) or info.get("debtToEquity"),

        "Revenue Growth %": (info.get("revenueGrowth") * 100) if info.get("revenueGrowth") is not None else None,
        "Earnings Growth %": (info.get("earningsGrowth") * 100) if info.get("earningsGrowth") is not None else None,
    }

    # Round floats for clean display
    for k, v in ratios.items():
        if isinstance(v, float):
            ratios[k] = round(v, 2)

    log.info("Calculated %d ratios for %s", len(ratios), data["ticker"])
    return ratios


# ==================================================================
# 3. CHARTS
# ==================================================================
def generate_charts(data: dict, output_dir: Path) -> list:
    """
    Two compact charts sized for a one-page report:
      1. Price chart with 50-day / 200-day moving averages
      2. Revenue vs Net Income (last up-to-4 fiscal years), if available
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_paths = []
    history = data["history"]
    fin = data["financials"]

    # --- Chart 1: price + moving averages ---
    fig, ax = plt.subplots(figsize=(6.3, 2.6))
    ax.plot(history.index, history["Close"], label="Close", color="#264653", linewidth=1.2)
    if len(history) >= 50:
        ax.plot(history.index, history["Close"].rolling(50).mean(),
                label="50-day MA", color="#2A9D8F", linewidth=1)
    if len(history) >= 200:
        ax.plot(history.index, history["Close"].rolling(200).mean(),
                label="200-day MA", color="#E76F51", linewidth=1)
    ax.set_title(f"{data['ticker']} - 1-Year Price", fontsize=10)
    ax.legend(fontsize=6, loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.tick_params(labelsize=7)
    plt.tight_layout()
    path = output_dir / "chart_price.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    # --- Chart 2: revenue vs net income ---
    if fin is not None and not fin.empty:
        revenue = None
        net_income = None
        for name in ["Total Revenue", "TotalRevenue"]:
            if name in fin.index:
                revenue = fin.loc[name]
                break
        for name in ["Net Income", "NetIncome", "Net Income Common Stockholders"]:
            if name in fin.index:
                net_income = fin.loc[name]
                break

        if revenue is not None and net_income is not None:
            years = [c.year if hasattr(c, "year") else str(c) for c in revenue.index][:4]
            rev_vals = revenue.values[:4] / 1e9
            ni_vals = net_income.reindex(revenue.index).values[:4] / 1e9

            fig, ax = plt.subplots(figsize=(6.3, 2.6))
            x = range(len(years))
            width = 0.35
            ax.bar([i - width / 2 for i in x], rev_vals, width, label="Revenue ($B)", color="#2E86AB")
            ax.bar([i + width / 2 for i in x], ni_vals, width, label="Net Income ($B)", color="#F4A261")
            ax.set_xticks(list(x))
            ax.set_xticklabels([str(y) for y in years], fontsize=7)
            ax.set_title("Revenue vs Net Income (Annual)", fontsize=10)
            ax.legend(fontsize=6)
            ax.tick_params(labelsize=7)
            plt.tight_layout()
            path = output_dir / "chart_financials.png"
            fig.savefig(path, dpi=150)
            plt.close(fig)
            chart_paths.append(path)

    log.info("Generated %d charts", len(chart_paths))
    return chart_paths


# ==================================================================
# 4. NEWS SUMMARY
# ==================================================================
def fetch_news(ticker: str, max_items: int = 4) -> list:
    """
    Pull recent headlines + short summaries from the Yahoo Finance RSS
    feed for the ticker. Falls back to yfinance's built-in `.news` list
    (headlines only, no summary) if the RSS feed returns nothing.
    """
    items = []
    try:
        feed_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:max_items]:
            summary = getattr(entry, "summary", "") or ""
            summary = textwrap.shorten(summary, width=220, placeholder="...")
            items.append({
                "title": getattr(entry, "title", ""),
                "summary": summary,
                "published": getattr(entry, "published", ""),
                "link": getattr(entry, "link", ""),
            })
    except Exception as e:
        log.warning("RSS news fetch failed: %s", e)

    if not items:
        try:
            t = yf.Ticker(ticker)
            raw_news = t.news or []
            for n in raw_news[:max_items]:
                # yfinance >= 0.2.40 nests fields under "content"
                content = n.get("content", n)
                items.append({
                    "title": content.get("title", ""),
                    "summary": "",
                    "published": content.get("pubDate", ""),
                    "link": (content.get("canonicalUrl") or {}).get("url", "")
                            if isinstance(content.get("canonicalUrl"), dict) else content.get("link", ""),
                })
        except Exception as e:
            log.warning("yfinance news fallback failed: %s", e)

    log.info("Fetched %d news items for %s", len(items), ticker)
    return items


# ==================================================================
# 5. ONE-PAGE PDF REPORT
# ==================================================================
def build_one_page_report(data: dict, ratios: dict, chart_paths: list,
                           news_items: list, output_path: Path) -> Path:
    """Assemble a single-page equity research snapshot as a PDF."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path), pagesize=A4,
        topMargin=1.2 * cm, bottomMargin=1.2 * cm,
        leftMargin=1.4 * cm, rightMargin=1.4 * cm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleC", parent=styles["Title"], fontSize=16, spaceAfter=2, leading=18)
    subtitle_style = ParagraphStyle("SubtitleC", parent=styles["Normal"], fontSize=8.5,
                                     textColor=colors.grey, spaceAfter=6)
    heading_style = ParagraphStyle("HeadC", parent=styles["Heading3"], fontSize=10.5, spaceBefore=4, spaceAfter=3)
    small_style = ParagraphStyle("SmallC", parent=styles["Normal"], fontSize=7.5, leading=9.5)
    news_title_style = ParagraphStyle("NewsTitle", parent=styles["Normal"], fontSize=8, leading=10,
                                       fontName="Helvetica-Bold", alignment=TA_LEFT)
    news_body_style = ParagraphStyle("NewsBody", parent=styles["Normal"], fontSize=7.5,
                                      leading=9, textColor=colors.HexColor("#333333"))

    story = []
    currency = ratios.get("Currency", "")
    price = ratios.get("Current Price")

    # --- Header ---
    story.append(Paragraph(f"{ratios.get('Company', data['ticker'])} ({data['ticker']})", title_style))
    story.append(Paragraph(
        f"{ratios.get('Sector', 'N/A')} &nbsp;|&nbsp; {ratios.get('Industry', 'N/A')} &nbsp;|&nbsp; "
        f"Price: {price} {currency} &nbsp;|&nbsp; Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        subtitle_style,
    ))

    # --- Ratio tables (two side-by-side columns for compactness) ---
    story.append(Paragraph("Key Financial Ratios", heading_style))

    def fmt(v):
        return "N/A" if v is None else str(v)

    left_keys = ["Market Cap", "52-Week High", "52-Week Low", "Beta",
                 "P/E (Trailing)", "P/E (Forward)", "P/B Ratio", "P/S Ratio"]
    right_keys = ["EPS (Trailing)", "Dividend Yield %", "Gross Margin %", "Net Margin %",
                  "Operating Margin %", "ROE %", "ROA %", "Current Ratio", "Debt-to-Equity"]

    left_rows = [[k, fmt(ratios.get(k))] for k in left_keys]
    right_rows = [[k, fmt(ratios.get(k))] for k in right_keys]

    def make_table(rows):
        t = Table(rows, colWidths=[3.6 * cm, 2.3 * cm])
        t.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.whitesmoke, colors.white]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        return t

    ratio_columns = Table(
        [[make_table(left_rows), make_table(right_rows)]],
        colWidths=[9 * cm, 8 * cm],
    )
    ratio_columns.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(ratio_columns)

    # --- Charts (side by side to save vertical space) ---
    if chart_paths:
        story.append(Paragraph("Charts", heading_style))
        img_cells = [Image(str(p), width=8.6 * cm, height=3.6 * cm) for p in chart_paths[:2]]
        if len(img_cells) == 1:
            story.append(img_cells[0])
        else:
            chart_row = Table([img_cells], colWidths=[8.8 * cm] * len(img_cells))
            story.append(chart_row)

    # --- News ---
    if news_items:
        story.append(Paragraph("Recent News", heading_style))
        for item in news_items:
            title = item["title"]
            published = item.get("published", "")
            summary = item.get("summary", "")
            story.append(Paragraph(f"{title}  <font color='grey'>({published})</font>", news_title_style))
            if summary:
                story.append(Paragraph(summary, news_body_style))
            story.append(Spacer(1, 3))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Data via Yahoo Finance (yfinance), unofficial and may be delayed. "
        "Generated automatically for informational purposes only - not investment advice.",
        small_style,
    ))

    doc.build(story)
    log.info("One-page report written to %s", output_path)
    return output_path


# ==================================================================
# ORCHESTRATION
# ==================================================================
def research_ticker(ticker: str):
    log.info("=" * 60)
    log.info("Researching %s", ticker)
    try:
        data = fetch_stock_data(ticker)
        ratios = calculate_ratios(data)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_dir = REPORTS_FOLDER / f"charts_{ticker}_{stamp}"
        chart_paths = generate_charts(data, chart_dir)

        news_items = fetch_news(ticker)

        output_path = REPORTS_FOLDER / f"{ticker.upper()}_{stamp}.pdf"
        build_one_page_report(data, ratios, chart_paths, news_items, output_path)

        import shutil
        shutil.rmtree(chart_dir, ignore_errors=True)

        log.info("Done: %s", output_path)
        return output_path

    except Exception as e:
        log.error("Failed to research %s: %s", ticker, e)
        return None


def main():
    tickers = sys.argv[1:]
    if not tickers:
        raw = input("Enter a stock ticker (or comma-separated list, e.g. AAPL,MSFT,INFY.NS): ").strip()
        tickers = [t.strip() for t in raw.split(",") if t.strip()]

    if not tickers:
        print("No ticker entered. Exiting.")
        return

    REPORTS_FOLDER.mkdir(parents=True, exist_ok=True)
    for ticker in tickers:
        research_ticker(ticker)


if __name__ == "__main__":
    main()
