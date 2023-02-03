import folium as fl
import streamlit as st
from streamlit_folium import st_folium
from owslib.wms import WebMapService

import numpy as np
import pandas as pd
import plotly.express as px


import matplotlib.pyplot as plt
import altair as alt
import joblib

import sys
sys.path.append('endlessline_eleven\\app\\pages\\utils')
import streamlit_functions


st.set_page_config(layout="wide", page_title="Forecasting", page_icon=":trend:")
st.markdown("<h1 style='color:#5DB44C'>Forecasting Waiting Times</h1>", unsafe_allow_html=True)

st.write(":chart_with_upwards_trend: Select ay combination of :green[**month, day, time, and attraction**], and find out what the waiting time will be!")

# Load Data
@st.cache(allow_output_mutation=True)
def load_df(path):
    df = pd.read_csv(path)
    return df

#Model data
df = load_df("../data/input_processed_data.csv")

## Load Model
@st.cache(allow_output_mutation=True)
def load_model(pkl_file_path):
    reg = joblib.load(pkl_file_path)
    return reg

pipeline = load_model("../models/pipelineines.pkl")


## Filters
# Dropdown
attraction_names = df['ENTITY_DESCRIPTION_SHORT'].unique()
attraction_names = ["Select All"] + list(attraction_names)

# Create a multi-select dropdown for attraction
selected_attraction = st.multiselect("Select attraction(s)", attraction_names, default="Select All")

if "Select All" not in selected_attraction:
    attraction_filters = [df['ENTITY_DESCRIPTION_SHORT'] == attraction for attraction in selected_attraction]
    attraction_filter = attraction_filters[0]
    for i in range(1, len(attraction_filters)):
        attraction_filter |= attraction_filters[i]
    filtered_df = df[attraction_filter]
else:
    filtered_df = df


months = df['month'].unique()
months =  ["Select All"] + list(months)

col1, col2 = st.columns(2)
with col1:
    selected_month = st.selectbox('Select month:', months)


days = df['day'].unique()
days = ["Select All"] + list(days)

with col2:
    selected_day = st.selectbox('Select day:', days)

hour_selected = st.slider("Select hour range", 9, 22, (9, 22))

predict = st.checkbox('Make Predictions')

# Filter the df based on the hours
if hour_selected != (9, 22):
    filtered_df = filtered_df[(filtered_df['hour'] >= hour_selected[0]) & (filtered_df['hour'] <= hour_selected[1])]

if predict:
    if selected_month != "Select All" and selected_day == "Select All":
        filtered_df = filtered_df[filtered_df['month'] == selected_month]
        predictions = pipeline.predict(filtered_df.drop(['WAIT_TIME_MAX'], axis=1))
        mean = np.mean(predictions)
        st.write(":clock1: With the selected filters we forecast the :green[**overall average waiting time**] to be: :green[**{:.2f}**] minutes".format(mean))

        df_preds = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Average Waiting Time': predictions})
        df_preds = df_preds.groupby('Attraction').mean()
        st.dataframe(df_preds, use_container_width=True)

        #Plot
        df_preds2 = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Day': filtered_df['day'], 'Average Waiting Time': predictions})

        # Create the dropdown using Plotly's updatemenus argument
        # Dropdown
        attraction_names2 = df_preds2['Attraction'].unique()
        attraction_names2 = list(attraction_names2)

        # Create a multi-select dropdown for attraction
        selected_attraction2 = st.selectbox("Select attraction to plot the prediction", attraction_names2, key=1)

        sub_filtered_df = df_preds2[df_preds2['Attraction'] == selected_attraction2].groupby('Day').mean().reset_index()

        chart = alt.Chart(sub_filtered_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('Day:O', title='Day'),
            y=alt.Y('Average Waiting Time:Q', title='Avg Wait Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='Day:O',
            y='Average Waiting Time:Q'
        )
        st.write(chart+line)

    elif selected_month != "Select All" and selected_day != "Select All":
        filtered_df = df[(df['month'] == selected_month) & (df['day'] == selected_day)]
        predictions = pipeline.predict(filtered_df.drop(['WAIT_TIME_MAX'], axis=1))
        mean = np.mean(predictions)
        st.write(":clock1: With the selected filters we forecast the :green[**overall average waiting time**] to be: :green[**{:.2f}**] minutes".format(mean))

        df_preds = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Average Waiting Time': predictions})
        df_preds = df_preds.groupby('Attraction').mean()
        st.dataframe(df_preds, use_container_width=True)

        #Plot
        df_preds2 = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Hour': filtered_df['hour'], 'Average Waiting Time': predictions})

        # Create the dropdown using Plotly's updatemenus argument
        # Dropdown
        attraction_names2 = df_preds2['Attraction'].unique()
        attraction_names2 = list(attraction_names2)

        # Create a multi-select dropdown for attraction
        selected_attraction2 = st.selectbox("Select attraction to plot the prediction", attraction_names2, key=2)

        sub_filtered_df = df_preds2[df_preds2['Attraction'] == selected_attraction2].groupby('Hour').mean().reset_index()

        chart = alt.Chart(sub_filtered_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('Hour:O', title='Hour'),
            y=alt.Y('Average Waiting Time:Q', title='Avg Wait Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='Hour:O',
            y='Average Waiting Time:Q'
        )
        st.write(chart+line)
        
    
    elif selected_month == "Select All" and selected_day != "Select All":
        filtered_df = df[df['day'] == selected_day]
        predictions = pipeline.predict(filtered_df.drop(['WAIT_TIME_MAX'], axis=1))
        mean = np.mean(predictions)
        st.write(":clock1: With the selected filters we forecast the :green[**overall average waiting time**] to be: :green[**{:.2f}**] minutes".format(mean))

        df_preds = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Average Waiting Time': predictions})
        df_preds = df_preds.groupby('Attraction').mean()
        st.dataframe(df_preds, use_container_width=True)

        #Plot
        df_preds2 = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Hour': filtered_df['hour'], 'Average Waiting Time': predictions})

        # Create the dropdown using Plotly's updatemenus argument
        # Dropdown
        attraction_names2 = df_preds2['Attraction'].unique()
        attraction_names2 = list(attraction_names2)

        # Create a multi-select dropdown for attraction
        selected_attraction2 = st.selectbox("Select attraction to plot the prediction", attraction_names2, key=3)

        sub_filtered_df = df_preds2[df_preds2['Attraction'] == selected_attraction2].groupby('Hour').mean().reset_index()

        chart = alt.Chart(sub_filtered_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('Hour:O', title='Hour'),
            y=alt.Y('Average Waiting Time:Q', title='Avg Wait Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='Hour:O',
            y='Average Waiting Time:Q'
        )
        st.write(chart+line)

    else:
        predictions = pipeline.predict(filtered_df.drop(['WAIT_TIME_MAX'], axis=1))
        mean = np.mean(predictions)
        st.write(":clock1: With the selected filters we forecast, the :green[**overall average waiting time**] to be: :green[**{:.2f}**] minutes".format(mean))

        df_preds = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Average Waiting Time': predictions})
        df_preds = df_preds.groupby('Attraction').mean()
        st.dataframe(df_preds.style.highlight_max(color='#FAD8F9', axis=0).highlight_min(color = '#D8FAD9', axis=0), use_container_width=True)

        #Plot
        df_preds2 = pd.DataFrame({'Attraction': filtered_df['ENTITY_DESCRIPTION_SHORT'], 'Month': filtered_df['month'], 'Average Waiting Time': predictions})

        # Create the dropdown using Plotly's updatemenus argument
        # Dropdown
        attraction_names2 = df_preds2['Attraction'].unique()
        attraction_names2 = list(attraction_names2)

        # Create a multi-select dropdown for attraction
        selected_attraction2 = st.selectbox("Select attraction to plot the prediction", attraction_names2, key=4)

        sub_filtered_df = df_preds2[df_preds2['Attraction'] == selected_attraction2].groupby('Month').mean().reset_index()

        chart = alt.Chart(sub_filtered_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('Month:O', title='Month'),
            y=alt.Y('Average Waiting Time:Q', title='Avg Wait Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='Month:O',
            y='Average Waiting Time:Q'
        )
        st.write(chart+line)
