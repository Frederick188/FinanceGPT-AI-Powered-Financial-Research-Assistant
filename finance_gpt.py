import streamlit as st
from finance_agent.stock_agent import ask_finance_agent
from finance_agent.ticker import get_ticker
from finance_agent.rag_agent import ask_documents

from finance_agent.charts import (
    load_stock_data,
    plot_candlestick,
    plot_price,
    plot_volume,
    plot_rsi,
    plot_macd,
    plot_moving_averages,
    plot_bollinger
)

# ------------------------------
# Page Configuration
# ------------------------------

st.set_page_config(
    page_title="FinanceGPT",
    page_icon="📈",
    layout="wide"
)

# ------------------------------
# Custom CSS
# ------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

.title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------
# Title
# ------------------------------

st.markdown(
    "<div class='title'>📈 FinanceGPT</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>AI-Powered Financial Research Assistant</div>",
    unsafe_allow_html=True
)

stock_tab, rag_tab, chart_tab = st.tabs(
    [
        "📄 Stock Analysis",
        "📄 Financial Documents",
        "📊 Charts"
    ]
)

# ------------------------------
# Chat History
# ------------------------------

with stock_tab:

    if "messages" not in st.session_state:

        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ------------------------------
    # Chat Input
    # ------------------------------

    prompt = st.chat_input(
        "Ask anything about a stock..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing market..."):

                response = ask_finance_agent(prompt)

                st.markdown(response)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":response
            }
        )
        
with rag_tab:

    st.header("📄 Financial Document Chat")

    st.write(
        "Upload a financial document (Annual Report, 10-K, 10-Q, Earnings Report) and ask questions about it."
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        save_path = "finance_agent/rag/documents/uploaded_report.pdf"

        with open(save_path, "wb") as f:

            f.write(uploaded_file.getbuffer())

        if st.button("Build Knowledge Base"):

            with st.spinner("Indexing document..."):

                from finance_agent.rag.ingest import main

                main()

            st.success("Knowledge base created successfully!")

        st.divider()

        if "rag_messages" not in st.session_state:

            st.session_state.rag_messages = []

        for message in st.session_state.rag_messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

        rag_prompt = st.chat_input(
            "Ask questions about this document...",
            key="rag_chat"
        )

        if rag_prompt:

            st.session_state.rag_messages.append(
                {
                    "role": "user",
                    "content": rag_prompt
                }
            )

            with st.chat_message("user"):

                st.markdown(rag_prompt)

            with st.chat_message("assistant"):

                with st.spinner("Searching document..."):

                    response = ask_documents(rag_prompt)

                    st.markdown(response)

            st.session_state.rag_messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )
    
        
with chart_tab:

    st.header("📊 Stock Charts")

    company = st.text_input(
        "Enter Company Name",
        placeholder="Apple, Nvidia, Microsoft..."
    )


    if st.button("Show Charts"):

        ticker = get_ticker(
            company.strip()
        )

        if ticker:

            df = load_stock_data(
                ticker
            )

            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
                [
                    "Candlestick",
                    "Price",
                    "Volume",
                    "RSI",
                    "MACD",
                    "Moving Averages",
                    "Bollinger Bands"
                ]
            )

            with tab1:
                plot_candlestick(df, ticker)

            with tab2:
                plot_price(df, ticker)

            with tab3:
                plot_volume(df)

            with tab4:
                plot_rsi(df)

            with tab5:
                plot_macd(df)
                
            with tab6:

                plot_moving_averages(df, ticker)

            with tab7:

                plot_bollinger(df, ticker)

        else:

            st.error(
                "Company not found."
            )

