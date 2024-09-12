from data_processing import fetch_company_data, calculate_financial_metrics, get_historical_revenue, get_asset_composition
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api():
    ticker = "AAPL"
    try:
        logger.info(f"Testing API with ticker: {ticker}")
        company_data = fetch_company_data(ticker)
        
        logger.info("Calculating financial metrics")
        financial_metrics = calculate_financial_metrics(company_data)
        logger.info(f"Financial metrics: {financial_metrics}")
        
        logger.info("Getting historical revenue")
        historical_revenue = get_historical_revenue(company_data)
        logger.info(f"Historical revenue: {historical_revenue}")
        
        logger.info("Getting asset composition")
        asset_composition = get_asset_composition(company_data)
        logger.info(f"Asset composition: {asset_composition}")
        
        logger.info("API test completed successfully")
    except Exception as e:
        logger.error(f"Error during API test: {str(e)}")

if __name__ == "__main__":
    test_api()
