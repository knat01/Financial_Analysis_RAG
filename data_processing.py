import requests
import pandas as pd
import numpy as np
import plotly.express as px
from openai import OpenAI

def fetch_financial_data(ticker, api_key):
    # Fetch data from Alpha Vantage API
    base_url = "https://www.alphavantage.co/query"

    # Income Statement
    params_is = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": api_key
    }
    response_is = requests.get(base_url, params=params_is)
    if response_is.status_code != 200:
        return None
    data_is = response_is.json()

    # Balance Sheet
    params_bs = {
        "function": "BALANCE_SHEET",
        "symbol": ticker,
        "apikey": api_key
    }
    response_bs = requests.get(base_url, params=params_bs)
    if response_bs.status_code != 200:
        return None
    data_bs = response_bs.json()

    # Cash Flow
    params_cf = {
        "function": "CASH_FLOW",
        "symbol": ticker,
        "apikey": api_key
    }
    response_cf = requests.get(base_url, params=params_cf)
    if response_cf.status_code != 200:
        return None
    data_cf = response_cf.json()

    financial_data = {
        'income_statement': data_is,
        'balance_sheet': data_bs,
        'cash_flow': data_cf
    }
    return financial_data

def process_financial_data(financial_data):
    print("Financial Data Structure:")
    print(financial_data.keys())
    print("Income Statement Structure:")
    print(financial_data['income_statement'].keys())
    
    # Check if 'annualReports' exists
    if 'annualReports' not in financial_data['income_statement']:
        print("Warning: 'annualReports' not found in income statement data")
        # Try to use quarterlyReports instead
        if 'quarterlyReports' in financial_data['income_statement']:
            print("Using quarterlyReports for income statement")
            income_statement = financial_data['income_statement']['quarterlyReports'][0]
        else:
            print("Error: No financial report data available")
            return pd.DataFrame({'Error': ['No financial report data available']}), []
    else:
        income_statement = financial_data['income_statement']['annualReports'][0]

    # Similar checks for balance sheet and cash flow
    if 'annualReports' not in financial_data['balance_sheet']:
        if 'quarterlyReports' in financial_data['balance_sheet']:
            balance_sheet = financial_data['balance_sheet']['quarterlyReports'][0]
        else:
            return pd.DataFrame({'Error': ['No balance sheet data available']}), []
    else:
        balance_sheet = financial_data['balance_sheet']['annualReports'][0]

    if 'annualReports' not in financial_data['cash_flow']:
        if 'quarterlyReports' in financial_data['cash_flow']:
            cash_flow = financial_data['cash_flow']['quarterlyReports'][0]
        else:
            return pd.DataFrame({'Error': ['No cash flow data available']}), []
    else:
        cash_flow = financial_data['cash_flow']['annualReports'][0]

    # Calculate metrics
    metrics = {}

    try:
        # Gross Profit Margin
        revenue = float(income_statement['totalRevenue'])
        cogs = float(income_statement['costOfRevenue'])
        gross_profit = revenue - cogs
        gross_profit_margin = (gross_profit / revenue) * 100
        metrics['Gross Profit Margin (%)'] = round(gross_profit_margin, 2)

        # Net Profit Margin
        net_income = float(income_statement['netIncome'])
        net_profit_margin = (net_income / revenue) * 100
        metrics['Net Profit Margin (%)'] = round(net_profit_margin, 2)

        # Current Ratio
        current_assets = float(balance_sheet['totalCurrentAssets'])
        current_liabilities = float(balance_sheet['totalCurrentLiabilities'])
        current_ratio = current_assets / current_liabilities
        metrics['Current Ratio'] = round(current_ratio, 2)

        # Debt-to-Equity Ratio
        total_liabilities = float(balance_sheet['totalLiabilities'])
        total_shareholder_equity = float(balance_sheet['totalShareholderEquity'])
        debt_to_equity = total_liabilities / total_shareholder_equity
        metrics['Debt-to-Equity Ratio'] = round(debt_to_equity, 2)

        # Operating Cash Flow Margin
        operating_cash_flow = float(cash_flow['operatingCashflow'])
        operating_cash_flow_margin = (operating_cash_flow / revenue) * 100
        metrics['Operating Cash Flow Margin (%)'] = round(operating_cash_flow_margin, 2)

    except KeyError as e:
        print(f"Error: Missing key in financial data: {e}")
        return pd.DataFrame({'Error': [f'Missing key in financial data: {e}']}), []
    except ValueError as e:
        print(f"Error: Invalid value in financial data: {e}")
        return pd.DataFrame({'Error': [f'Invalid value in financial data: {e}']}), []
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return pd.DataFrame({'Error': [f'Unexpected error occurred: {e}']}), []

    # Create charts
    charts = []

    try:
        # Bar chart for historical revenue trends
        revenue_trends = pd.DataFrame(financial_data['income_statement'].get('annualReports', financial_data['income_statement'].get('quarterlyReports', [])))
        revenue_trends['fiscalDateEnding'] = pd.to_datetime(revenue_trends['fiscalDateEnding'])
        revenue_trends['totalRevenue'] = revenue_trends['totalRevenue'].astype(float)
        revenue_trends = revenue_trends.sort_values('fiscalDateEnding')

        fig_revenue = px.bar(revenue_trends, x='fiscalDateEnding', y='totalRevenue', title='Historical Revenue')
        charts.append(fig_revenue)

        # Donut chart for asset composition
        assets = {
            'Current Assets': float(balance_sheet['totalCurrentAssets']),
            'Non-Current Assets': float(balance_sheet.get('totalNonCurrentAssets', 0))
        }
        fig_assets = px.pie(names=list(assets.keys()), values=list(assets.values()), hole=0.5, title='Asset Composition')
        charts.append(fig_assets)

    except Exception as e:
        print(f"Error creating charts: {e}")
        # If charts creation fails, we'll return the metrics without charts

    metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])

    return metrics_df, charts

def generate_financial_insights(metrics_df, openai_api_key):
    try:
        # Use OpenAI API to generate insights based on the metrics
        client = OpenAI(api_key=openai_api_key)

        # Convert metrics dataframe to text
        metrics_text = metrics_df.to_string(index=False)

        prompt = f"""
        Analyze the following financial metrics and provide insights about the company's financial health:

        {metrics_text}

        Focus on aspects like profitability, liquidity, and solvency.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            temperature=0.7,
        )

        insights = response.choices[0].message.content.strip()
        return insights
    except Exception as e:
        print(f"Error generating financial insights: {str(e)}")
        return "Unable to generate AI insights at this time. Please try again later."
