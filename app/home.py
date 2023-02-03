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
    - [Weather Impact](Weather_Impact) to find out how the weather is impacting E's activities, from waiting times to closure.
    - [Forecasting](Forecasting) to forecast attractions waiting times.
    - [Clients](Clients) a page dedicated to E's visitor to better plan their visit to E.
    """
)