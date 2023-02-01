import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from owslib.wms import WebMapService

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

import sys 
sys.path.append('../')
from features.build_data import * 
from features.streamlit_functions import *

st.set_page_config(layout="wide", page_title="Operation Performance Analysis", page_icon=":compass:")

st.markdown("<h1 style='color:#5DB44C'>Operation Performance Analysis</h1>", unsafe_allow_html=True)

# Load Data

@st.cache(allow_output_mutation=True)
def load_data(path):
    df = pd.read_csv(path)
    return df

df = load_data("../data/data_merged.csv")
#Preprocess
df = get_data_ready(df)


########################################### KPIS ##########################################

# Dropdown
attraction_names = df['ENTITY_DESCRIPTION_SHORT'].unique()
attraction_names = ["Select All"] + list(attraction_names)

## create a dropdown menu for the user to select the server name
selected_attraction = st.selectbox('Select attraction:', attraction_names)

if selected_attraction == "Select All":
    df = df
else:
    df = df[df['ENTITY_DESCRIPTION_SHORT'] == selected_attraction]


######################### DELTA #################################
years = df['year'].unique()
years =  ["Select All"] + list(years)
selected_year = st.selectbox('Select year:', years)

months = df['month'].unique()
months =  ["Select All"] + list(months)
selected_month = st.selectbox('Select month:', months)

days = df['day'].unique()
days = ["Select All"] + list(days)
selected_day = st.selectbox('Select day:', days)

col1, col2 = st.columns([2, 2])
col1.subheader(":scales: :green[Average Capacity]")
col2.subheader(':gear: :green[Adjusted Capacity]')

avg_wait_time = calculate_metrics(df, selected_year, selected_month, selected_day)[0]
capacity_utilization = calculate_metrics(df, selected_year, selected_month, selected_day)[1]
avg_adjust_capacity_utilization = calculate_metrics(df, selected_year, selected_month, selected_day)[2]
sum_attendance = calculate_metrics(df, selected_year, selected_month, selected_day)[3]

delta = None
delta1 = None
delta2 = None
delta3 = None 

delta = calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, capacity_utilization, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3)[0]
delta1 = calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, capacity_utilization, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3)[1]
delta2 = calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, capacity_utilization, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3)[2]

col1.metric("Capacity Utilization" , '{:,.0f}%'.format(capacity_utilization), delta=delta1)
col2.metric("Adjusted Capacity Utilization" , '{:,.0f}%'.format(capacity_utilization), delta=delta2)

#################################### Capacity #######################################

if selected_year == "Select All" and selected_month == "Select All" and selected_day == "Select All":
    filtered_df = df
elif selected_year != "Select All" and selected_month == "Select All" and selected_day == "Select All":
    filtered_df = df[(df['year'] == selected_year)]
elif selected_year == "Select All" and selected_month != "Select All" and selected_day == "Select All":
    filtered_df = df[(df['month'] == selected_month)]
elif selected_year == "Select All" and selected_month == "Select All" and selected_day != "Select All":
    filtered_df = df[(df['day'] == selected_day)]
elif selected_year != "Select All" and selected_month != "Select All" and selected_day == "Select All":
    filtered_df = df[(df['year'] == selected_year) &
                    (df['month'] == selected_month)]
elif selected_year != "Select All" and selected_month == "Select All" and selected_day != "Select All":
    filtered_df = df[(df['year'] == selected_year) &
                    (df['day'] == selected_day)]
elif selected_year == "Select All" and selected_month != "Select All" and selected_day != "Select All":
    filtered_df = df[(df['day'] == selected_day) &
                    (df['month'] == selected_month)]
elif selected_year != "Select All" and selected_month != "Select All" and selected_day != "Select All":
    filtered_df = df[(df['year'] == selected_year) &
                    (df['month'] == selected_month) &
                    (df['day'] == selected_day)]

if selected_attraction == "Select All":
    average_capacity = filtered_df['CAPACITY'].mean()
    average_adjust_capacity = filtered_df['ADJUST_CAPACITY'].mean()
    average_capacity_diff = average_capacity - average_adjust_capacity
    guest = filtered_df['GUEST_CARRIED'].mean()
    full = guest / average_adjust_capacity
    capacity_available =  average_adjust_capacity/average_capacity
    # Display the average values
    st.write("Average Capacity:", average_capacity)
    st.write("Average Adjusted Capacity:", average_adjust_capacity)
    st.write("Average Capacity Difference:", average_capacity_diff)
    st.write("Average Number of Guest Carried:", guest)
    st.write("Average Full:", full)
    st.write("Capacity Available:", capacity_available)
else:
    # Display the data in a table for the selected attraction
    st.write("Data for the selected attraction:", selected_attraction)
    st.write(filtered_df[['WORK_DATE', 'ENTITY_DESCRIPTION_SHORT', 'CAPACITY', 'ADJUST_CAPACITY', 'NB_UNITS', 'NB_MAX_UNIT']])

