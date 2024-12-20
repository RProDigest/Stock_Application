import yfinance as yf
import streamlit as st
from datetime import datetime
from datetime import date
import datetime as dt
import pandas as pd
import numpy as np
import altair as alt

st.write(
    """
# Stock Price Application Analyzer

Shown are the stock **closing price** and ***volume*** of a Company!

"""
)


@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


@st.cache_data  # Use st.cache_data instead of st.cache
def load_ftse100data():
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    html = pd.read_html(url, header=0)
    df = html[3]
    return df


# Set the start date to 2020-01-01
start = dt.date(2020, 1, 1)
st.sidebar.markdown("# Start and End Date:")
w1 = st.sidebar.date_input("Start", start, min_value=date(1970, 1, 1))

# Set the end date to 2024-12-20
end = dt.date(2024, 12, 20)
w2 = st.sidebar.date_input("End", end, min_value=date(1970, 1, 1))

# Set the default ticker symbol to Qualcomm (QCOM)
tickerSymbol = "QCOM"
name = "Qualcomm"

option = st.sidebar.selectbox(
    "Select a Stock Market:", ["S&P 500", "FTSE 100"], index=0
)
st.sidebar.write("You selected:", option)

if option == "S&P 500":
    df = load_data()
    coms = df["Symbol"]
    names = df["Security"]

    # Find the index of "QCOM" in the list
    qcom_index = coms.tolist().index("QCOM")  # Get the position in the list

    option1 = st.sidebar.selectbox(
        "Select a Company:", coms, index=qcom_index
    )  # Use QCOM's index

    i = [i for i, j in enumerate(coms) if j == option1]
    name = names[i]
    tickerSymbol = option1
    st.sidebar.write(option1)

elif option == "FTSE 100":
    df = load_ftse100data()
    coms = df["EPIC"]
    names = df["Company"]

    option2 = st.sidebar.selectbox("Select a Company:", coms, index=0)

    i = [i for i, j in enumerate(coms) if j == option2]
    name = names[i]
    tickerSymbol = option2
    st.sidebar.write(option2)

# Get stock data
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period="1d", start=w1, end=w2)

st.write(name)
st.write(
    """
## Closing Price
"""
)
if len(tickerDf) > 1:
    st.line_chart(tickerDf.Close)
    st.write(
        "Percentage Change : "
        + str(
            int((tickerDf.Close[-1] - tickerDf.Close[0]) / tickerDf.Close[0] * 1000)
            / 10.0
        )
        + "%"
    )
else:
    st.write("Data not available...")

st.write(
    """
## Volume Price
"""
)
if len(tickerDf) > 1:
    st.line_chart(tickerDf.Volume)
else:
    st.write("Data not available...")

toplist = []
if st.button("Top Performers"):

    for i in range(len(coms)):

        tickerData = yf.Ticker(coms[i])
        tickerDf = tickerData.history(period="1d", start=w1, end=w2)

        if len(tickerDf) < 1:
            continue

        percentChange = (
            int((tickerDf.Close[-1] - tickerDf.Close[0]) / tickerDf.Close[0] * 1000)
            / 10.0
        )
        name = names[i]
        toplist.append([coms[i], name, percentChange])

    results = sorted(toplist, key=lambda l: l[2], reverse=True)
    st.write(results[0:19])

    x = [x[0] for x in results[0:19]]
    y = [x[1] for x in results[0:19]]
    z = [x[2] for x in results[0:19]]

    data = pd.DataFrame(
        {
            "Company Symbol": x,
            "Company Name": y,
            "Percentage Change": z,
        }
    )

    st.write(data)
    st.write(
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("Company Symbol", sort=None),
            y="Percentage Change",
        )
    )
