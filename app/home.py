import streamlit as st

st.sidebar.title("Contact Us!")
st.sidebar.info(
    """
    augustin.de-la-brosse@hec.edu
    cesar.bareau@hec.edu 
    camille.keisser@hec.edu
    simon.mack@hec.edu
    charlotte.simon@hec.edu
    julia.tournant@hec.edu
    """
)


st.markdown(
    """
    # 💻 Welcome to your newest tool to Optimize the IT Infrastructure Consumption

    Navigate through the **sidebar tabs** to explore how your servers currently work, how ressources are distributed, and find out how you can optimize their configuration while reducing your cost and your impact on the environment.
    
    ## Want to know more about our features?
    - [Data Exploration](Data_Exploration) to analyze every aspects of Natixis' servers and understand how ressources are being used.
    - [Optimization](Optimization) to optimize servers configuration.
    - [Max Consumption Prediction](Max_Consumption_Prediction) to predict how much a server will consume in the future so you can assign ressources ahead of time.
    - [Cost and Power Consumption](Cost_and_Power_Consumption) to find out how you can minimize your cost and reduce your impact on the environment!
    """
)