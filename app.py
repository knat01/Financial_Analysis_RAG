import streamlit as st
from data_processing import fetch_financial_data, process_financial_data, generate_financial_insights
from report_analysis import process_annual_report, answer_question_from_report
import os

def api_keys_page():
    st.header("API Keys")
    openai_api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get('openai_api_key', ''))
    financial_api_key = st.text_input("Financial Data API Key (e.g., Alpha Vantage)", type="password", value=st.session_state.get('financial_api_key', ''))
    
    if st.button("Save API Keys"):
        st.session_state['openai_api_key'] = openai_api_key
        st.session_state['financial_api_key'] = financial_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
        st.success("API Keys saved successfully!")

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
            
            st.subheader("AI-Generated Insights")
            insights = generate_financial_insights(metrics_df, st.session_state['openai_api_key'])
            st.write(insights)
        else:
            st.error("Failed to fetch financial data. Please check the ticker symbol and try again.")

def document_analysis_page():
    st.header("Document Analysis")
    
    if 'openai_api_key' not in st.session_state:
        st.warning("Please enter your OpenAI API key in the API Keys tab.")
        return
    
    uploaded_file = st.file_uploader("Upload an annual report PDF", type=["pdf"])
    
    if uploaded_file:
        st.write("Processing annual report...")
        vectorstore = process_annual_report(uploaded_file, st.session_state['openai_api_key'])
        st.session_state['vectorstore'] = vectorstore
        st.success("Annual report processed successfully!")
    
    if 'vectorstore' in st.session_state:
        question = st.text_input("Enter your question about the report")
        
        if question:
            st.write("Generating answer...")
            answer, sources = answer_question_from_report(question, st.session_state['vectorstore'], st.session_state['openai_api_key'])
            st.write("**Answer:**")
            st.write(answer)
            st.write("**Relevant Sources:**")
            for i, source in enumerate(sources, 1):
                st.write(f"Source {i}:")
                st.text(source)

def main():
    st.title("Financial Insights Application")

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state['page'] = "API Keys"

    # Create sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["API Keys", "Financial Data", "Document Analysis"])

    # Update session state
    st.session_state['page'] = page

    # Display the selected page
    if st.session_state['page'] == "API Keys":
        api_keys_page()
    elif st.session_state['page'] == "Financial Data":
        financial_data_page()
    elif st.session_state['page'] == "Document Analysis":
        document_analysis_page()

if __name__ == "__main__":
    main()
