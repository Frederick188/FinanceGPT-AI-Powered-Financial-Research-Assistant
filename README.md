# FinanceGPT: AI-Powered Financial Research Assistant

FinanceGPT is an end-to-end AI-powered financial analysis platform that combines Large Language Models, Machine Learning, Sentiment Analysis, Technical Indicators, and Retrieval-Augmented Generation (RAG) to assist investors in making informed decisions.

The application provides two major capabilities:

* **Stock Analysis Agent** – Performs live market analysis using financial news, technical indicators, and machine learning.
* **Financial Document Agent (RAG)** – Answers questions from Annual Reports, SEC filings, earnings reports, and other financial documents using semantic search.

---

## Features

### 🤖 Stock Analysis Agent

* Live financial news using Finnhub API
* FinBERT-based news sentiment analysis
* Technical indicators using Yahoo Finance

  * RSI
  * MACD
  * SMA20 & SMA50
  * EMA20 & EMA50
  * Daily Return
  * Volatility
  * Trading Volume
* XGBoost-based next-day stock return prediction
* AI-generated confidence score
* BUY / HOLD / SELL recommendation
* Interactive Streamlit interface
* Live stock charts

  * Candlestick
  * Closing Price
  * Volume
  * RSI
  * MACD
  * Bollinger Bands
  * Moving Average Overlay

---

### 📄 Financial Document Agent (RAG)

* Upload financial documents (PDF)
* Semantic search using FAISS
* Sentence Transformer embeddings
* Context-aware question answering
* Source-grounded responses
* Supports:

  * Annual Reports
  * SEC Filings (10-K / 10-Q)
  * Earnings Reports
  * Financial Statements

---

## Tech Stack

* Python
* Streamlit
* LangChain
* RAG
* Google Gemini API
* FinBERT
* XGBoost
* FAISS
* Sentence Transformers
* Hugging Face Transformers
* Yahoo Finance API
* Finnhub API
* Plotly
* Pandas
* Scikit-learn

---



# Project Architecture

## 1. Model Training Pipeline

```text
                    Historical Stock Data
                  (Yahoo Finance API)
                            │
                            ▼
                Historical Financial News
                     (Finnhub API)
                            │
                            ▼
                 FinBERT Sentiment Analysis
                            │
                            ▼
                  Daily Sentiment Score
                            │
                            │
      ┌─────────────────────┴─────────────────────┐
      │                                           │
      ▼                                           ▼
Technical Indicators                     News Features
(RSI, SMA20, SMA50, EMA20,               Sentiment Score
 EMA50, MACD, Volatility,                News Count
 Return, Volume)
      │                                           │
      └─────────────────────┬─────────────────────┘
                            │
                            ▼
               Feature Engineering & Dataset
                    (final_dataset.csv)
                            │
                            ▼
               Train XGBoost Regression Model
                            │
                            ▼
                 xgboost_model.pkl (Saved Model)
                            │
                            ▼
              Model Evaluation & Backtesting
                            │
      ┌─────────────────────┼─────────────────────┐
      ▼                     ▼                     ▼
Feature Importance   Strategy vs Market   Trading Signals
(feature_importance) (backtest_results)    BUY/HOLD/SELL
                            │
                            ▼
             Streamlit Dashboard (app.py)
```

---

## 2. FinanceGPT Runtime Architecture

```text
                          Streamlit UI
                       (finance_gpt.py)
                               │
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
       ▼                       ▼                        ▼
 Stock Analysis Tab     Financial Documents      Live Charts
                              (RAG)
       │                       │                        │
       ▼                       ▼                        ▼
  Stock Agent            Upload PDF              Yahoo Finance
       │                       │                        │
       │                       ▼                        ▼
       │                 PDF Loader               Live Market Data
       │                       │                        │
       │                 Text Splitter           Plotly Visualizations
       │                       │
       │            Sentence Transformers
       │                       │
       │                  FAISS Vector DB
       │                       │
       │                   RAG Retriever
       │                       │
       │                       ▼
       │                  Gemini API
       │
       ▼
┌───────────────────────────────────────────────────────────────┐
│                  Stock Analysis Pipeline                      │
├───────────────────────────────────────────────────────────────┤
│ Finnhub API → Latest Financial News                          │
│             ↓                                                │
│        FinBERT Sentiment Analysis                            │
│             ↓                                                │
│ Yahoo Finance → Technical Indicators                         │
│             ↓                                                │
│ XGBoost (.pkl) → Next-Day Return Prediction                  │
│             ↓                                                │
│ Gemini API → Financial Analysis & Recommendation             │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. Overall System Architecture

```text
                    ┌─────────────────────────┐
                    │       FinanceGPT        │
                    │     Streamlit UI        │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼────────────────────────┐
         │                       │                        │
         ▼                       ▼                        ▼
  Stock Analysis          Financial Documents       Live Charts
      Agent                  RAG Agent
         │                       │
         ▼                       ▼
   Finnhub API             Upload PDF
         │                       │
         ▼                       ▼
      FinBERT             PDF Processing
         │                       │
         ▼                       ▼
 Yahoo Finance      Sentence Transformers
         │                       │
         ▼                       ▼
Technical Indicators         FAISS
         │                       │
         ▼                       ▼
 XGBoost Prediction      Semantic Retrieval
         │                       │
         └───────────────┬───────┘
                         ▼
                   Gemini API
                         │
                         ▼
         AI-Powered Financial Insights
```

---

## Installation

```bash
git clone <repository-url>

cd FinanceGPT

pip install -r requirements.txt
```

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_API_KEY
FINNHUB_API_KEY=YOUR_API_KEY
```

---

## Run the Application

```bash
streamlit run trained_model_app.py
streamlit run finance_gpt.py
```

---

## Example Queries

### Stock Analysis

* Analyze Amazon
* How is Amazon performing today?
* Compare Microsoft and Google
* What's your analysis of Amazon?


### Financial Documents

* What are Amazon's major business risks?
* Summarize NVIDIA's annual report.
* What are Microsoft's revenue segments?
* Explain Apple's legal risks.
* What are the key risk factors mentioned in the report?

---

## Future Enhancements

* Portfolio Management
* Stock Comparison Dashboard
* Earnings Call Transcript Analysis
* Real-time Market Alerts
* Multi-Agent Routing
* Explainable AI (XAI)
* Portfolio Optimization
* Cloud Deployment (AWS/Azure)

---

## Disclaimer

This project is developed for educational and research purposes.

The generated investment recommendations are AI-assisted analyses and should not be considered financial advice. Always conduct independent research before making investment decisions.
