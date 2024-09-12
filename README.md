# Financial Insights Application

## Introduction
The Financial Insights Application is a Streamlit-based tool that provides key metrics, visualizations, and AI-generated insights for user-specified companies. It leverages financial data APIs and OpenAI's language models to offer a comprehensive analysis of a company's financial health.

## Features
- Fetch and analyze financial data for any publicly traded company
- Display key financial metrics including profitability, liquidity, and efficiency ratios
- Generate interactive visualizations of financial trends
- Provide AI-powered insights on company performance
- Analyze uploaded annual reports using natural language processing

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/your-username/financial-insights-app.git
   cd financial-insights-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:5000`

3. Enter your API keys in the "API Keys" tab

4. Navigate to the "Financial Data" tab and enter a company's ticker symbol

5. Explore the financial metrics, charts, and AI-generated insights

6. For annual report analysis, go to the "Document Analysis" tab, upload a PDF, and ask questions about the report

## Project Structure
- `app.py`: Main Streamlit application file
- `data_processing.py`: Functions for fetching and processing financial data
- `report_analysis.py`: Functions for analyzing uploaded annual reports
- `test_api.py`: API testing utility

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Streamlit](https://streamlit.io/)
- [Alpha Vantage API](https://www.alphavantage.co/)
- [OpenAI API](https://openai.com/)
- [Plotly](https://plotly.com/)
- [LangChain](https://github.com/hwchase17/langchain)
