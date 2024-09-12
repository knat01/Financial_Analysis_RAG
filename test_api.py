import os
from data_processing import fetch_financial_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api():
    ticker = "AAPL"
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    
    if not api_key:
        logger.error("ALPHA_VANTAGE_API_KEY is not set in the environment variables.")
        return "API key is missing. Please check your API Keys in the application."

    try:
        logger.info(f"Testing API with ticker: {ticker}")
        financial_data = fetch_financial_data(ticker, api_key)
        
        if financial_data is None:
            logger.error("Failed to fetch financial data.")
            return "The API failed to retrieve the data. Please check your internet connection and try again."
        
        logger.info("Financial data structure:")
        logger.info(financial_data.keys())
        
        for statement in ['income_statement', 'balance_sheet', 'cash_flow']:
            if statement not in financial_data:
                logger.error(f"{statement} is missing from the financial data.")
                return f"The API response is missing {statement}. Please try again later."
            
            if 'annualReports' not in financial_data[statement] and 'quarterlyReports' not in financial_data[statement]:
                logger.error(f"No reports found in {statement}.")
                return f"No financial reports found in {statement}. The API might be experiencing issues."
        
        logger.info("API test completed successfully")
        return "Financial data retrieved successfully. If you're not seeing the data in the application, there might be an issue with data processing or display."
    
    except Exception as e:
        logger.error(f"Error during API test: {str(e)}")
        return f"An unexpected error occurred: {str(e)}. Please try again later."

if __name__ == "__main__":
    result = test_api()
    print(result)
