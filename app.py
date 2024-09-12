import streamlit as st
from data_processing import fetch_financial_data, process_financial_data, generate_financial_insights
from report_analysis import process_annual_report, answer_question_from_report
import os

def main():
    st.title("Financial Insights Application")

    # Section to input API keys
    st.sidebar.header("API Keys")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
    financial_api_key = st.sidebar.text_input("Financial Data API Key (e.g., Alpha Vantage)", type="password", value=os.environ.get("ALPHA_VANTAGE_API_KEY", ""))

    if not openai_api_key:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()

    if not financial_api_key:
        st.warning("Please enter your Financial Data API key to continue.")
        st.stop()

    # Set OpenAI API key
    os.environ['OPENAI_API_KEY'] = openai_api_key

    st.header("Company Ticker Input")
    ticker = st.text_input("Enter the ticker symbol of a company (e.g., AAPL, MSFT)")

    if ticker:
        # Fetch financial data
        st.write(f"Fetching financial data for {ticker}...")
        financial_data = fetch_financial_data(ticker, financial_api_key)

        if financial_data is not None:
            # Process financial data to get metrics and charts
            metrics_df, charts = process_financial_data(financial_data)

            # Display metrics
            st.subheader("Key Financial Metrics")
            st.table(metrics_df)

            # Display charts
            st.subheader("Financial Charts")
            for chart in charts:
                st.plotly_chart(chart)

            # Generate insights using OpenAI
            st.subheader("AI-Generated Insights")
            insights = generate_financial_insights(metrics_df, openai_api_key)
            st.write(insights)
        else:
            st.error("Failed to fetch financial data. Please check the ticker symbol and try again.")

    st.header("Optional: Upload Annual Report")
    uploaded_file = st.file_uploader("Upload an annual report PDF", type=["pdf"])

    if uploaded_file:
        st.write("Processing annual report...")
        # Process the annual report
        vectorstore = process_annual_report(uploaded_file, openai_api_key)

        # User question input
        st.subheader("Ask a Question about the Annual Report")
        question = st.text_input("Enter your question about the report")

        if question:
            # Get answer from the report
            st.write("Generating answer...")
            answer, sources = answer_question_from_report(question, vectorstore, openai_api_key)
            st.write("**Answer:**")
            st.write(answer)
            st.write("**Relevant Sources:**")
            for i, source in enumerate(sources, 1):
                st.write(f"Source {i}:")
                st.text(source)

if __name__ == "__main__":
    main()
