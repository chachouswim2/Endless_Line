import folium as fl
import streamlit as st
from streamlit_folium import st_folium
from owslib.wms import WebMapService

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import joblib

import sys
sys.path.append('../')
from features.streamlit_functions import *



st.set_page_config(layout="wide", page_title="Forecasting", page_icon=":trend:")
st.markdown("<h1 style='color:#5DB44C'>Forecasting Waiting Times</h1>", unsafe_allow_html=True)

st.write(":chart_with_upwards_trend: Select ay combination of :green[**year, month, day, time, attraction, and weather**], and find out what the waiting time will be!")

# Load Data
@st.cache(allow_output_mutation=True)
def load_df(path):
    df = pd.read_csv(path)
    return df

df = load_df("../data/data_merged.csv")

#Preprocess
df = get_data_ready(df)

## Load Model
#@st.cache(allow_output_mutation=True)
#def load_model():
    #model = keras.models.load_model('silo_segmentation_last_adagrad.h5', compile=False)
    #return model
    
#model = load_model()


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


# Years, months, day, time
years = list(['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'])
selected_years = st.selectbox('Select the year you plan to visit:', years)

months = df['month'].unique()
months =  ["Select All"] + list(months)
selected_month = st.selectbox('Select month:', months)

days = df['day'].unique()
days = ["Select All"] + list(days)
selected_day = st.selectbox('Select day:', days)

hour_selected = st.slider("Select hour range", 9, 22, (9, 22))

#Weather
weather = df['weather_description'].unique()
weather = ['Select All'] + list(weather)
selected_weather = st.selectbox('Select a weather:', weather)


# Filter the df based on the selected filters
filtered_df = df[df['year'] == selected_years]
if selected_month != "Select All":
    filtered_df = df[df['month'] == selected_month]
if selected_day != "Select All":
    filtered_df = filtered_df[filtered_df['day'] == selected_day]
if hour_selected != (9, 22):
    filtered_df = filtered_df[(filtered_df['hour'] >= hour_selected[0]) & (filtered_df['hour'] <= hour_selected[1])]
if selected_weather != "Select All":
    filtered_df = filtered_df[filtered_df['weather_description']==  selected_weather]

#Predict
#preds = model.predict(filtered_df)

# If all the attractions are selected
if "Select All" in selected_attraction:
    st.write(f":clock1: With the selected filters we forecast, the :green[**overall average waiting time**] to be: :green[**xx**] minutes")

# If a couple of attractions are selected
else:
    avg_table = filtered_df.groupby("ENTITY_DESCRIPTION_SHORT")['WAIT_TIME_MAX'].mean()
    avg_table = avg_table.to_frame()
    avg_table.reset_index(inplace=True)
    avg_table.columns = ['Attraction', 'Predicted Average Waiting Time']
    avg_table['Predicted Average Waiting Time'] = avg_table['Predicted Average Waiting Time'].round(2)

    st.write("Predicted Average waiting time for each attraction:")
    st.table(avg_table)
    st.write(f"With the selected filters we predict the :green[**overall average waiting time**] to be: :green[**xx**] minutes")
