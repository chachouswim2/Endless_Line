import streamlit as st

st.sidebar.title("Contact Us!")
st.sidebar.info(
    """
    ines.benito@hec.edu
    lea.chader@hec.edu 
    remi.khellaf@hec.edu
    mohamed-salah.mahmoudi@hec.edu
    charlotte.simon@hec.edu
    """
)


st.markdown(
    """
    # 🎡 Welcome to E's newest tool to keep track of your park activities, performance, maintenance, and waiting times. 

    Navigate through the **sidebar tabs** to explore how PortAventura World is currently performing and how its activities can be optimized.
    
    ## Want to know more about your features?
    - [Customer Performance](Customer_Performance) to explore how E's activities are impacting customers.
    - [Operation Performance](Operation_Performance) to explore how E's operational activities.
    - [Forecasting](Forecasting) to forecast attractions waiting times
    - [Leverage Information](Leverage_Information) to read about identified use cases to leverage the forecasting findings and improve E's KPIS.
    """
)