import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI

def fetch_financial_data(ticker, api_key):
    base_url = "https://www.alphavantage.co/query"
    
    # Fetch Income Statement
    params_is = {
        "function": "INCOME_STATEMENT",
        "symbol": ticker,
        "apikey": api_key
    }
    response_is = requests.get(base_url, params=params_is)
    if response_is.status_code != 200:
        return None
    data_is = response_is.json()
    
    # Fetch Balance Sheet
    params_bs = {
        "function": "BALANCE_SHEET",
        "symbol": ticker,
        "apikey": api_key
    }
    response_bs = requests.get(base_url, params=params_bs)
    if response_bs.status_code != 200:
        return None
    data_bs = response_bs.json()
    
    # Fetch Cash Flow
    params_cf = {
        "function": "CASH_FLOW",
        "symbol": ticker,
        "apikey": api_key
    }
    response_cf = requests.get(base_url, params=params_cf)
    if response_cf.status_code != 200:
        return None
    data_cf = response_cf.json()
    
    # Fetch Global Quote for current price
    params_quote = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": api_key
    }
    response_quote = requests.get(base_url, params=params_quote)
    if response_quote.status_code != 200:
        return None
    data_quote = response_quote.json()

    financial_data = {
        'income_statement': data_is,
        'balance_sheet': data_bs,
        'cash_flow': data_cf,
        'quote': data_quote
    }
    return financial_data

def process_financial_data(financial_data):
    metrics = {}
    charts = []

    try:
        # Extract data from financial statements
        income_statement = financial_data['income_statement']['annualReports'][0]
        balance_sheet = financial_data['balance_sheet']['annualReports'][0]
        cash_flow = financial_data['cash_flow']['annualReports'][0]

        # Calculate existing metrics
        revenue = float(income_statement['totalRevenue'])
        cogs = float(income_statement['costOfRevenue'])
        gross_profit = revenue - cogs
        gross_profit_margin = (gross_profit / revenue) * 100
        metrics['Gross Profit Margin (%)'] = round(gross_profit_margin, 2)

        net_income = float(income_statement['netIncome'])
        net_profit_margin = (net_income / revenue) * 100
        metrics['Net Profit Margin (%)'] = round(net_profit_margin, 2)

        current_assets = float(balance_sheet['totalCurrentAssets'])
        current_liabilities = float(balance_sheet['totalCurrentLiabilities'])
        current_ratio = current_assets / current_liabilities
        metrics['Current Ratio'] = round(current_ratio, 2)

        total_liabilities = float(balance_sheet['totalLiabilities'])
        total_shareholder_equity = float(balance_sheet['totalShareholderEquity'])
        debt_to_equity = total_liabilities / total_shareholder_equity
        metrics['Debt-to-Equity Ratio'] = round(debt_to_equity, 2)

        operating_cash_flow = float(cash_flow['operatingCashflow'])
        operating_cash_flow_margin = (operating_cash_flow / revenue) * 100
        metrics['Operating Cash Flow Margin (%)'] = round(operating_cash_flow_margin, 2)

        # Calculate new advanced metrics
        total_assets = float(balance_sheet['totalAssets'])
        
        # Return on Equity (ROE)
        roe = (net_income / total_shareholder_equity) * 100
        metrics['Return on Equity (%)'] = round(roe, 2)

        # Earnings Per Share (EPS)
        common_stock_outstanding = float(balance_sheet['commonStockSharesOutstanding'])
        eps = net_income / common_stock_outstanding
        metrics['Earnings Per Share ($)'] = round(eps, 2)

        # Price to Earnings (P/E) Ratio
        if 'Global Quote' in financial_data['quote']:
            current_price = float(financial_data['quote']['Global Quote']['05. price'])
            pe_ratio = current_price / eps
            metrics['Price to Earnings Ratio'] = round(pe_ratio, 2)

        # Return on Assets (ROA)
        roa = (net_income / total_assets) * 100
        metrics['Return on Assets (%)'] = round(roa, 2)

        # Create charts
        # Historical Revenue Trend
        historical_revenue = [
            {'year': report['fiscalDateEnding'][:4], 'revenue': float(report['totalRevenue'])}
            for report in financial_data['income_statement']['annualReports'][:5]  # Last 5 years
        ]
        historical_revenue.reverse()  # Oldest to newest
        
        fig_revenue = px.bar(
            historical_revenue, 
            x='year', 
            y='revenue', 
            title='Historical Revenue Trend'
        )
        charts.append(fig_revenue)

        # Profit Margins Over Time
        profit_margins = [
            {
                'year': report['fiscalDateEnding'][:4],
                'Gross Profit Margin': (float(report['totalRevenue']) - float(report['costOfRevenue'])) / float(report['totalRevenue']) * 100,
                'Net Profit Margin': float(report['netIncome']) / float(report['totalRevenue']) * 100
            }
            for report in financial_data['income_statement']['annualReports'][:5]  # Last 5 years
        ]
        profit_margins.reverse()  # Oldest to newest
        
        fig_margins = px.line(
            profit_margins, 
            x='year', 
            y=['Gross Profit Margin', 'Net Profit Margin'],
            title='Profit Margins Over Time'
        )
        charts.append(fig_margins)

        # ROE vs P/E Ratio Scatter Plot
        if 'Price to Earnings Ratio' in metrics:
            fig_scatter = px.scatter(
                x=[metrics['Price to Earnings Ratio']],
                y=[metrics['Return on Equity (%)']],
                text=[f"P/E: {metrics['Price to Earnings Ratio']}<br>ROE: {metrics['Return on Equity (%)']}%"],
                title='ROE vs P/E Ratio'
            )
            fig_scatter.update_traces(textposition='top center')
            charts.append(fig_scatter)

    except KeyError as e:
        print(f"Error: Missing key in financial data: {e}")
        return pd.DataFrame({'Error': [f'Missing key in financial data: {e}']}), []
    except ValueError as e:
        print(f"Error: Invalid value in financial data: {e}")
        return pd.DataFrame({'Error': [f'Invalid value in financial data: {e}']}), []
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return pd.DataFrame({'Error': [f'Unexpected error occurred: {e}']}), []

    metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
    return metrics_df, charts

def generate_financial_insights(metrics_df, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    
    metrics_text = metrics_df.to_string(index=False)
    
    prompt = f"""
    Analyze the following financial metrics and provide insights about the company's financial health:
    
    {metrics_text}
    
    Focus on aspects like profitability, liquidity, and solvency.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a financial analyst."}, {"role": "user", "content": prompt}],
        max_tokens=500,
        n=1,
        temperature=0.7,
    )
    
    insights = response.choices[0].message.content.strip()
    return insights
