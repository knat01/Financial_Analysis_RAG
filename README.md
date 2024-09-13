# Financial Insights Application

## Introduction

The **Financial Insights Application** is a powerful, AI-driven tool that helps users gain comprehensive insights into publicly traded companies. By combining financial data APIs with natural language processing through OpenAI's language models, this application offers key metrics, interactive visualizations, and AI-generated insights to help users understand a company’s financial health. The application is built using **Streamlit** for rapid development and a user-friendly interface.

## Screen Recording

[![Watch the demo](https://img.youtube.com/vi/etLcaK7pp3U/maxresdefault.jpg)](https://www.youtube.com/watch?v=etLcaK7pp3U)
Click the image above to watch a screen recording of the Financial Insights Application in action. In this demo, you'll see how the app retrieves real-time financial data, provides AI-powered insights, and generates interactive visualizations for company analysis.


## Key Features

- **Financial Data Retrieval**: Fetch real-time financial data for any publicly traded company using the Alpha Vantage API.
- **Interactive Visualizations**: Generate dynamic charts to display trends in key financial metrics such as profitability, liquidity, and efficiency ratios.
- **AI-Powered Insights**: Leverage OpenAI's language models to provide in-depth, natural language insights into a company’s performance.
- **Document Analysis**: Upload and analyze annual reports or other financial documents using natural language processing (NLP) to extract key information and answer specific questions.
- **Comprehensive Metrics**: Display detailed financial ratios such as **Price-to-Earnings (P/E)**, **Debt-to-Equity**, **Current Ratio**, and more.

## Technologies Used

### 1. **Streamlit**
   - **Streamlit** serves as the web framework, providing a simple yet effective interface for users to interact with the data. It enables rapid development of interactive applications and is ideal for real-time data visualizations.

### 2. **Alpha Vantage API**
   - The **Alpha Vantage API** is used to retrieve up-to-date financial data such as stock prices, balance sheets, and income statements. This API allows users to access a wide range of data points, which are displayed in the application for easy analysis.

### 3. **OpenAI API**
   - OpenAI's powerful language models are used to generate AI-driven insights based on financial data and uploaded documents. These models help users interpret financial reports by generating summaries and answering user queries in natural language.

### 4. **Plotly**
   - **Plotly** is used for generating interactive charts that visualize financial data trends over time. Users can easily track financial performance metrics and make data-driven decisions.

### 5. **LangChain**
   - **LangChain** enables seamless integration of language models with the financial analysis process. It is used for document processing, allowing the application to answer user queries about uploaded financial reports.

### 6. **LlamaIndex**
   - **LlamaIndex** powers the document analysis feature. It enables efficient indexing of annual reports and other financial documents, allowing the application to quickly search and retrieve relevant information for answering user questions.

## Installation

### Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/financial-insights-app.git
   cd financial-insights-app
    pip install -r requirements.txt
Use code with caution.
Markdown
Set up Environment Variables: Create a .env file in the root directory and add your API keys for Alpha Vantage and OpenAI:
Use code with caution.
Bash
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
OPENAI_API_KEY=your_openai_api_key
3. **Run the Streamlit Application**: Launch the application using Streamlit:
```bash
streamlit run app.py
```
Access the Application: Open your web browser and navigate to:
```
http://localhost:8501
```
5. **Enter API Keys**: In the "API Keys" tab, input your Alpha Vantage and OpenAI API keys.

6. **Analyze Financial Data**: Navigate to the "Financial Data" tab, enter a company’s stock ticker symbol, and explore the visualized financial metrics and AI-generated insights.

7. **Document Analysis**: For document analysis, go to the "Document Analysis" tab, upload a financial report (e.g., PDF), and ask specific questions about the content.

## Project Structure
```
.
├── app.py                    # Main Streamlit application
├── data_processing.py         # Fetches and processes financial data from APIs
├── report_analysis.py         # NLP analysis of uploaded financial documents
├── requirements.txt           # Python dependencies
├── test_api.py                # Utility script to test API functionality
├── .env                       # Environment variables (API keys)
└── README.md                  # This project documentation

```
app.py: The entry point of the application. It handles user interactions, API requests, and the display of financial metrics and insights.
data_processing.py: Contains functions for fetching financial data from the Alpha Vantage API and processing it for visualization and analysis.
report_analysis.py: Implements the NLP analysis of annual reports and other financial documents using OpenAI’s models.
test_api.py: A script used to test the integration with Alpha Vantage and OpenAI APIs.

## Contributing
We welcome contributions! Please follow these steps to contribute:

1. **Fork the repository**: Create a copy of the repository on your GitHub account.
2. **Create a new branch**:  Branch off from the `main` branch to work on your changes (e.g., `git checkout -b feature/new-feature`).
3. **Make your changes**: Implement your feature or bug fix.
4. **Commit your changes**:  Save your work with a clear commit message that explains what you changed (e.g., `git commit -am 'Add new feature for X'`).
5. **Push your branch**:  Push your changes to your forked repository (`git push origin feature/new-feature`).
6. **Open a Pull Request**:  Go to the original repository on GitHub, create a pull request from your branch to the `main` branch of the original repository.  

For major changes, please open an issue first to discuss what you would like to implement.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
- Streamlit
- Alpha Vantage API
- OpenAI API
- Plotly
- LangChain
- LlamaIndex
