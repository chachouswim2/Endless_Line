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
df['WORK_DATE'] = pd.to_datetime(df['WORK_DATE'])
df['year'] = df['WORK_DATE'].dt.year
df['month'] = df['WORK_DATE'].dt.month
df['day'] = df['WORK_DATE'].dt.day


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

col1, col2, col3 = st.columns(3)

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

col1.metric("Average waiting time (mns)" , round(avg_wait_time, 2), delta=delta, delta_color="inverse")
col2.metric("Capacity Utilization" , '{:,.0f}%'.format(capacity_utilization), delta=delta1)
col3.metric("Adjusted Capacity Utilization" , '{:,.0f}%'.format(capacity_utilization), delta=delta2)

#################################### WAITING TIMES #######################################




