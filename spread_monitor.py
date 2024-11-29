import MetaTrader5 as mt5
import pandas as pd
import streamlit as st

# MT5 Installation Paths
mt5_path = r"C:\Program Files\FundedNext MT5 Terminal\terminal64.exe"

# Account Details
account = {
    "login": 13109044,
    "password": "ubmAX18##",
    "server": "FundedNext-Server 2"
}

# Fetch spreads and prepare data
def fetch_spreads():
    if not mt5.initialize(path=mt5_path):
        st.error(f"Failed to initialize MT5: {mt5.last_error()}")
        return None

    if not mt5.login(login=account["login"], password=account["password"], server=account["server"]):
        st.error(f"Failed to log in to account: {mt5.last_error()}")
        mt5.shutdown()
        return None

    symbols = mt5.symbols_get()
    spread_data = []

    for symbol in symbols:
        tick = mt5.symbol_info_tick(symbol.name)
        symbol_info = mt5.symbol_info(symbol.name)
        if tick and symbol_info:
            spread = round((tick.ask - tick.bid) / symbol_info.point, 1)
            spread_data.append([symbol.name, spread])

    mt5.shutdown()
    return pd.DataFrame(spread_data, columns=["Symbol", "Spread (Pipettes)"])

# Streamlit layout
st.title("Prop Firm Spread Monitor")
st.write("Monitor spreads for various trading accounts.")

if st.button("Fetch Spread Data"):
    spread_df = fetch_spreads()
    if spread_df is not None:
        st.dataframe(spread_df)

        # Option to download data
        csv = spread_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Spread Data as CSV",
            data=csv,
            file_name="spread_data.csv",
            mime="text/csv"
        )
