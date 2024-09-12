import streamlit as st
from data_processing import fetch_financial_data, process_financial_data, generate_financial_insights
from report_analysis import process_annual_report, answer_question_from_report
from test_api import test_api
import os

def main():
    st.set_page_config(page_title="Financial Insights Application", layout="wide")
    st.title("Financial Insights Application")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["API Keys", "Financial Data", "Annual Report Analysis"])

    with tab1:
        api_keys_page()

    with tab2:
        financial_data_page()

    with tab3:
        annual_report_page()

def api_keys_page():
    st.header("API Keys")
    
    st.session_state['openai_api_key'] = st.text_input("Enter your OpenAI API Key:", type="password")
    st.session_state['financial_api_key'] = st.text_input("Enter your Alpha Vantage API Key:", type="password")
    
    if st.button("Test API Connection"):
        result = test_api()
        st.write(result)

def financial_data_page():
    st.header("Financial Data Analysis")
    
    if 'openai_api_key' not in st.session_state or 'financial_api_key' not in st.session_state:
        st.warning("Please enter your API keys in the API Keys tab.")
        return
    
    ticker = st.text_input("Enter the ticker symbol of a company (e.g., AAPL, MSFT)")
    
    if ticker:
        st.write(f"Fetching financial data for {ticker}...")
        financial_data = fetch_financial_data(ticker, st.session_state['financial_api_key'])
        
        if financial_data is not None:
            metrics_df, charts = process_financial_data(financial_data)
            
            st.subheader("Key Financial Metrics")
            st.table(metrics_df)
            
            st.subheader("Financial Charts")
            for chart in charts:
                st.plotly_chart(chart)
            
            st.subheader("Advanced Metrics Explanation")
            st.write("""
            - **Return on Equity (ROE)**: Measures how efficiently a company uses its equity to generate profits.
            - **Earnings Per Share (EPS)**: Indicates how much profit a company allocates to each outstanding share of common stock.
            - **Price to Earnings (P/E) Ratio**: Compares a company's share price to its earnings per share.
            - **Return on Assets (ROA)**: Shows how efficiently a company uses its assets to generate profits.
            """)
            
            st.subheader("AI-Generated Insights")
            insights = generate_financial_insights(metrics_df, st.session_state['openai_api_key'])
            st.write(insights)
        else:
            st.error("Failed to fetch financial data. Please check the ticker symbol and try again.")

def annual_report_page():
    st.header("Annual Report Analysis")
    
    if 'openai_api_key' not in st.session_state:
        st.warning("Please enter your OpenAI API key in the API Keys tab.")
        return
    
    uploaded_file = st.file_uploader("Upload an annual report (PDF)", type="pdf")
    
    if uploaded_file is not None:
        st.write("Processing the uploaded annual report...")
        vectorstore = process_annual_report(uploaded_file, st.session_state['openai_api_key'])
        st.session_state['vectorstore'] = vectorstore
        st.success("Annual report processed successfully!")
        
        question = st.text_input("Ask a question about the annual report:")
        if question:
            if 'vectorstore' in st.session_state:
                answer, sources = answer_question_from_report(question, st.session_state['vectorstore'], st.session_state['openai_api_key'])
                st.write("Answer:", answer)
                st.write("Sources:")
                for i, source in enumerate(sources, 1):
                    st.write(f"Source {i}:", source)
            else:
                st.error("Please upload and process an annual report before asking questions.")

if __name__ == "__main__":
    main()
