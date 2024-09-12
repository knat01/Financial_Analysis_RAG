import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
    for statement in ['income_statement', 'balance_sheet', 'cash_flow']:
        print(f"{statement.capitalize()} Structure:")
        print(financial_data[statement].keys())
    
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
        revenue = float(income_statement['totalRevenue'])
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating revenue: {e}")
        revenue = None

    try:
        cogs = float(income_statement['costOfRevenue'])
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating cost of revenue: {e}")
        cogs = None

    if revenue is not None and cogs is not None:
        gross_profit = revenue - cogs
        gross_profit_margin = (gross_profit / revenue) * 100 if revenue != 0 else None
        metrics['Gross Profit Margin (%)'] = round(gross_profit_margin, 2) if gross_profit_margin is not None else None

    try:
        net_income = float(income_statement['netIncome'])
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating net income: {e}")
        net_income = None

    if revenue is not None and net_income is not None:
        net_profit_margin = (net_income / revenue) * 100 if revenue != 0 else None
        metrics['Net Profit Margin (%)'] = round(net_profit_margin, 2) if net_profit_margin is not None else None

    try:
        current_assets = float(balance_sheet['totalCurrentAssets'])
        current_liabilities = float(balance_sheet['totalCurrentLiabilities'])
        current_ratio = current_assets / current_liabilities if current_liabilities != 0 else None
        metrics['Current Ratio'] = round(current_ratio, 2) if current_ratio is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating current ratio: {e}")

    try:
        total_liabilities = float(balance_sheet['totalLiabilities'])
        total_shareholder_equity = float(balance_sheet['totalShareholderEquity'])
        debt_to_equity = total_liabilities / total_shareholder_equity if total_shareholder_equity != 0 else None
        metrics['Debt-to-Equity Ratio'] = round(debt_to_equity, 2) if debt_to_equity is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating debt-to-equity ratio: {e}")

    try:
        operating_cash_flow = float(cash_flow['operatingCashflow'])
        operating_cash_flow_margin = (operating_cash_flow / revenue) * 100 if revenue != 0 else None
        metrics['Operating Cash Flow Margin (%)'] = round(operating_cash_flow_margin, 2) if operating_cash_flow_margin is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating operating cash flow margin: {e}")

    try:
        total_assets = float(balance_sheet['totalAssets'])
        roa = (net_income / total_assets) * 100 if total_assets != 0 else None
        metrics['Return on Assets (%)'] = round(roa, 2) if roa is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating return on assets: {e}")

    try:
        roe = (net_income / total_shareholder_equity) * 100 if total_shareholder_equity != 0 else None
        metrics['Return on Equity (%)'] = round(roe, 2) if roe is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating return on equity: {e}")

    try:
        common_stock_shares_outstanding = float(balance_sheet['commonStockSharesOutstanding'])
        eps = net_income / common_stock_shares_outstanding if common_stock_shares_outstanding != 0 else None
        metrics['Earnings Per Share (EPS)'] = round(eps, 2) if eps is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating earnings per share: {e}")

    try:
        market_cap = float(balance_sheet.get('marketCapitalization', 0))
        pe_ratio = market_cap / net_income if net_income != 0 else None
        metrics['Price to Earnings (P/E) Ratio'] = round(pe_ratio, 2) if pe_ratio is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating P/E ratio: {e}")

    try:
        ebitda = float(income_statement.get('ebitda', 0))
        total_debt = float(balance_sheet.get('shortLongTermDebtTotal', 0))
        debt_to_ebitda = total_debt / ebitda if ebitda != 0 else None
        metrics['Debt to EBITDA Ratio'] = round(debt_to_ebitda, 2) if debt_to_ebitda is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating Debt to EBITDA ratio: {e}")

    try:
        capital_expenditure = float(cash_flow.get('capitalExpenditures', 0))
        free_cash_flow = operating_cash_flow - capital_expenditure
        metrics['Free Cash Flow'] = round(free_cash_flow, 2)
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating Free Cash Flow: {e}")

    try:
        free_cash_flow_yield = (free_cash_flow / market_cap) * 100 if market_cap != 0 else None
        metrics['Free Cash Flow Yield (%)'] = round(free_cash_flow_yield, 2) if free_cash_flow_yield is not None else None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error calculating Free Cash Flow Yield: {e}")

    if all(metric is None for metric in metrics.values()):
        print("No valid financial metrics could be calculated")
        return pd.DataFrame({'Error': ['No valid financial metrics could be calculated']}), []

    # Create charts
    charts = []

    try:
        revenue_trends = pd.DataFrame(financial_data['income_statement'].get('annualReports', []))
        if revenue_trends.empty:
            revenue_trends = pd.DataFrame(financial_data['income_statement'].get('quarterlyReports', []))
        revenue_trends['fiscalDateEnding'] = pd.to_datetime(revenue_trends['fiscalDateEnding'])
        revenue_trends['totalRevenue'] = revenue_trends['totalRevenue'].astype(float)
        revenue_trends = revenue_trends.sort_values('fiscalDateEnding')

        fig_revenue = px.bar(revenue_trends, x='fiscalDateEnding', y='totalRevenue', title='Historical Revenue')
        charts.append(fig_revenue)
    except Exception as e:
        print(f"Error creating revenue chart: {e}")

    try:
        assets = {
            'Current Assets': float(balance_sheet['totalCurrentAssets']),
            'Non-Current Assets': float(balance_sheet.get('totalNonCurrentAssets', 0))
        }
        fig_assets = px.pie(names=list(assets.keys()), values=list(assets.values()), hole=0.5, title='Asset Composition')
        charts.append(fig_assets)
    except Exception as e:
        print(f"Error creating asset composition chart: {e}")

    try:
        profitability_metrics = pd.DataFrame(financial_data['income_statement'].get('annualReports', financial_data['income_statement'].get('quarterlyReports', [])))
        profitability_metrics['fiscalDateEnding'] = pd.to_datetime(profitability_metrics['fiscalDateEnding'])
        profitability_metrics['grossProfitMargin'] = (profitability_metrics['grossProfit'].astype(float) / profitability_metrics['totalRevenue'].astype(float)) * 100
        profitability_metrics['netProfitMargin'] = (profitability_metrics['netIncome'].astype(float) / profitability_metrics['totalRevenue'].astype(float)) * 100
        profitability_metrics = profitability_metrics.sort_values('fiscalDateEnding')

        fig_profitability = go.Figure()
        fig_profitability.add_trace(go.Scatter(x=profitability_metrics['fiscalDateEnding'], y=profitability_metrics['grossProfitMargin'], mode='lines+markers', name='Gross Profit Margin'))
        fig_profitability.add_trace(go.Scatter(x=profitability_metrics['fiscalDateEnding'], y=profitability_metrics['netProfitMargin'], mode='lines+markers', name='Net Profit Margin'))
        fig_profitability.update_layout(title='Profitability Metrics Over Time', xaxis_title='Date', yaxis_title='Percentage (%)')
        charts.append(fig_profitability)
    except Exception as e:
        print(f"Error creating profitability metrics chart: {e}")

    try:
        debt_ebitda_data = pd.DataFrame(financial_data['balance_sheet'].get('annualReports', financial_data['balance_sheet'].get('quarterlyReports', [])))
        debt_ebitda_data['fiscalDateEnding'] = pd.to_datetime(debt_ebitda_data['fiscalDateEnding'])
        debt_ebitda_data['shortLongTermDebtTotal'] = debt_ebitda_data['shortLongTermDebtTotal'].astype(float)
        
        income_data = pd.DataFrame(financial_data['income_statement'].get('annualReports', financial_data['income_statement'].get('quarterlyReports', [])))
        income_data['fiscalDateEnding'] = pd.to_datetime(income_data['fiscalDateEnding'])
        income_data['ebitda'] = income_data['ebitda'].astype(float)
        
        debt_ebitda_data = pd.merge(debt_ebitda_data, income_data[['fiscalDateEnding', 'ebitda']], on='fiscalDateEnding')
        debt_ebitda_data['debtToEBITDA'] = debt_ebitda_data['shortLongTermDebtTotal'] / debt_ebitda_data['ebitda']
        debt_ebitda_data = debt_ebitda_data.sort_values('fiscalDateEnding')

        fig_debt_ebitda = px.line(debt_ebitda_data, x='fiscalDateEnding', y='debtToEBITDA', title='Debt to EBITDA Ratio Over Time')
        charts.append(fig_debt_ebitda)
    except Exception as e:
        print(f"Error creating Debt to EBITDA chart: {e}")

    try:
        cash_flow_data = pd.DataFrame(financial_data['cash_flow'].get('annualReports', financial_data['cash_flow'].get('quarterlyReports', [])))
        cash_flow_data['fiscalDateEnding'] = pd.to_datetime(cash_flow_data['fiscalDateEnding'])
        cash_flow_data['operatingCashflow'] = cash_flow_data['operatingCashflow'].astype(float)
        cash_flow_data['capitalExpenditures'] = cash_flow_data['capitalExpenditures'].astype(float)
        cash_flow_data['freeCashFlow'] = cash_flow_data['operatingCashflow'] - cash_flow_data['capitalExpenditures']
        cash_flow_data = cash_flow_data.sort_values('fiscalDateEnding')

        fig_free_cash_flow = px.bar(cash_flow_data, x='fiscalDateEnding', y='freeCashFlow', title='Free Cash Flow Trend')
        charts.append(fig_free_cash_flow)
    except Exception as e:
        print(f"Error creating Free Cash Flow chart: {e}")

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

        Focus on aspects like profitability, liquidity, solvency, and efficiency. Provide a comprehensive analysis with specific recommendations for improvement.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing insights on company performance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750,
            n=1,
            temperature=0.7,
        )

        insights = response.choices[0].message.content.strip()
        return insights
    except Exception as e:
        print(f"Error generating financial insights: {str(e)}")
        return "Unable to generate AI insights at this time. Please try again later."
