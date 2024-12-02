import streamlit as st
import pandas as pd
import MetaTrader5 as mt5
import time

# Define MetaTrader 5 paths and account details
mt5_paths = {
    "FTMO": r"C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe",
    "5%ers": r"C:\Program Files\Tickmill MT5 Terminal\terminal64.exe",
    "FundedNext": r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe",
    "Alpha Capital": r"C:\Program Files\MetaTrader 5 IC Markets Global\terminal64.exe"
}

accounts = {
    "FTMO": {"login": 1510140547, "password": "6y*8P1V9?", "server": "FTMO-Demo"},
    "5%ers": {"login": 24088398, "password": "Investor5ers.", "server": "FivePercentOnline-Real"},
    "FundedNext": {"login": 13109044, "password": "ubmAX18##", "server": "FundedNext-Server 2"},
    "Alpha Capital": {"login": 1836665, "password": "Ftz1uK7y~U", "server": "ACGMarkets-Main"}
}

# Function to fetch spreads
def fetch_spreads():
    combined_data = []
    for account_name, details in accounts.items():
        if not mt5.initialize(path=mt5_paths[account_name]):
            st.error(f"Failed to initialize MT5 for {account_name}: {mt5.last_error()}")
            continue

        if not mt5.login(login=details["login"], password=details["password"], server=details["server"]):
            st.error(f"Failed to log in to {account_name}: {mt5.last_error()}")
            mt5.shutdown()
            continue

        symbols = mt5.symbols_get()
        account_spreads = {}
        for symbol in symbols:
            symbol_info = mt5.symbol_info_tick(symbol.name)
            if symbol_info:
                bid = symbol_info.bid
                ask = symbol_info.ask
                point = mt5.symbol_info(symbol.name).point
                spread = (ask - bid) / point if point else None
                if spread is not None:
                    account_spreads[symbol.name.split(".")[0]] = (
                        f"{spread:.1f}".rstrip("0").rstrip(".")
                    )  # Format to remove trailing zeros
                else:
                    account_spreads[symbol.name.split(".")[0]] = "N/A"

        combined_data.append(pd.DataFrame.from_dict(account_spreads, orient="index", columns=[account_name]))
        mt5.shutdown()

    if combined_data:
        df = pd.concat(combined_data, axis=1)
        df.fillna("N/A", inplace=True)
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Symbol"}, inplace=True)  # Ensure Symbol column exists
        return df
    return pd.DataFrame(columns=["Symbol"])  # Ensure empty DataFrame has 'Symbol'

# Streamlit Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: lime;
        text-align: center;
        background-color: black;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    th, td {
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<div class="main-title">Prop Firm Spread Monitor</div>', unsafe_allow_html=True)

# Search Bar
search_input = st.text_input("Search Symbol 🔍", "").upper()

# Data Display
data_placeholder = st.empty()

# Main refresh loop
while True:
    spread_data = fetch_spreads()

    if not spread_data.empty:
        if search_input:
            filtered_data = spread_data[spread_data["Symbol"].str.contains(search_input, na=False)]
        else:
            filtered_data = spread_data

        # Display Data
        data_placeholder.table(
            filtered_data.style
            .hide(axis="index")  # Completely hides the index column
            .set_properties(**{"text-align": "center"})
            .set_table_styles(
                [
                    {"selector": "th", "props": [("background-color", "black"), ("color", "lime")]},
                    {"selector": "td", "props": [("text-align", "center"), ("border", "1px solid black")]},
                ]
            )
        )
    else:
        data_placeholder.warning("No data available to display.")

    # Update every 100ms
    time.sleep(0.1)
