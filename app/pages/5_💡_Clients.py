import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from owslib.wms import WebMapService

import numpy as np
import pandas as pd
from PIL import Image

import matplotlib.pyplot as plt
import calendar
from datetime import date, timedelta
import time
import plotly
import plotly.express as px

import sys 
sys.path.append('../')
from features.build_data import * 
from features.streamlit_functions import *


st.set_page_config(layout="wide", page_title="Clients", page_icon=":flag:")
st.markdown("<h1 style='color:#5DB44C'>Use our newest technology to plan your visit to E</h1>", unsafe_allow_html=True)

# Load df
@st.cache(allow_output_mutation=True)
def load_df(path):
    df = pd.read_csv(path)
    return df

df = load_df("../data/data_merged.csv")
df['WORK_DATE'] = pd.to_datetime(df['WORK_DATE'])
df['year'] = df['WORK_DATE'].dt.year
df['month'] = df['WORK_DATE'].dt.month
df['day'] = df['WORK_DATE'].dt.day 
df['DEB_TIME'] = pd.to_datetime(df['DEB_TIME'])
df['hour'] = df['DEB_TIME'].dt.hour

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
selected_month = st.selectbox('Select month:', months)

days = df['day'].unique()
days = ["Select All"] + list(days)
selected_day = st.selectbox('Select day:', days)

weather = df['weather_description'].unique()
weather = ['Select All'] + list(weather)
selected_weather = st.selectbox('Select a weather:', weather)

# Create the slider widget for 'hour'
hour_selected = st.slider("Select hour range", 9, 22, (9, 22))

# Filter the df based on the selected filters
if selected_month != "Select All":
    filtered_df = df[df['month'] == selected_month]
if selected_day != "Select All":
    filtered_df = filtered_df[filtered_df['day'] == selected_day]
if selected_weather != "Select All":
    filtered_df = filtered_df[filtered_df['weather_description']==  selected_weather]
if hour_selected != (9, 22):
    filtered_df = filtered_df[(filtered_df['hour'] >= hour_selected[0]) & (filtered_df['hour'] <= hour_selected[1])]

# Calculate the average waiting time for each selected attraction
average_waiting_time = round(filtered_df.groupby('ENTITY_DESCRIPTION_SHORT')['WAIT_TIME_MAX'].mean(),2)

# If all the attractions are selected
if "Select All" in selected_attraction:
    st.write(f":clock1: With the selected filters and based on our previous data, the :green[**overall average waiting time**] is: :green[**{round(average_waiting_time.mean(), 2)}**] minutes")

# If a couple of attractions are selected
else:
    avg_table = filtered_df.groupby("ENTITY_DESCRIPTION_SHORT")['WAIT_TIME_MAX'].mean()
    avg_table = avg_table.to_frame()
    avg_table.reset_index(inplace=True)
    avg_table.columns = ['Attraction', 'Average Waiting Time']
    avg_table['Average Waiting Time'] = avg_table['Average Waiting Time'].round(2)

    st.write("Average waiting time for each attraction:")
    st.table(avg_table)
    st.write(f"With the selected filters and based on our previous data, the :green[**overall average waiting time**] is: :green[**{round(average_waiting_time.mean(), 2)}**] minutes")

###################################################### FORECAST MODEL #######################################################
st.empty()
st.markdown("##")

st.markdown("<h2 style='color:#5DB44C'> Use our Forecasting tool to find out what will be your Waiting Time on the day of your visit!</h2>", unsafe_allow_html=True)

years = list(['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'])
selected_years = st.selectbox('Select the year you plan to visit:', years)

st.write(":clock1: Based on your selection, we believe that :green[**your waiting time should be, on average**], ...")


##################################################### COMING SOON ##########################################################
st.markdown("""---""")

st.markdown("<h3 style='color:#5DB44C'> COMING SOON: We optimize your trip to E's so your waiting time is minimum</h3>", unsafe_allow_html=True)

st.write("We know that you hate waiting in line to tto enjoy your favorite ride. And we do to! This is why, at E, we are commited to making your experience better by reducing the time you spend waiting in line.")
st.write("Our team of engineers and data scientists is working on developping a model that will :green[**optimize your day-trip at E by suggesting an order of attraction that would reduce your waiting time**].")
st.write("For that, nothing simpler. You'll be able to select a day, time range, and specific attractions that you'd like to experiment and we will give you the optimized attraction order.")
st.write("Don't wait and discover below what our :green[**app**] will look like!")