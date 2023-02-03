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
sys.path.append('endlessline_eleven\\app\\pages\\utils')
import streamlit_functions

st.set_page_config(layout="wide", page_title="Operation Performance Analysis", page_icon=":compass:")

st.markdown("<h1 style='color:#5DB44C'>Operation Performance Analysis</h1>", unsafe_allow_html=True)

# Load Data

@st.cache(allow_output_mutation=True)
def load_data(path):
    df = pd.read_csv(path)
    return df

df = load_data("../data/data_merged.csv")
#Preprocess
df = streamlit_functions.get_data_ready(df)


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

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
col1.subheader(":scales: :green[Guest Carried]")
col2.subheader(':gear: :green[Adjusted Capacity Utilisation]')
col3.subheader(':100: :green[Capacity vs. Adjusted Capacity]')
col4.subheader(':large_green_circle: :green[Capacity Available]')

avg_wait_time = streamlit_functions.calculate_metrics(df, selected_year, selected_month, selected_day)[0]
guest = streamlit_functions.calculate_metrics(df, selected_year, selected_month, selected_day)[1]
avg_adjust_capacity_utilization = streamlit_functions.calculate_metrics(df, selected_year, selected_month, selected_day)[2]
sum_attendance = streamlit_functions.calculate_metrics(df, selected_year, selected_month, selected_day)[3]
per_cap_adj = streamlit_functions.calculate_metrics(df, selected_year, selected_month, selected_day)[4]

delta = None
delta1 = None
delta2 = None
delta3 = None 

delta = streamlit_functions.calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, guest, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3)[0]
delta1 = streamlit_functions.calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, guest, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3)[1]
delta2 = streamlit_functions.calculate_delta(df, selected_year, selected_month, selected_day, avg_wait_time, guest, avg_adjust_capacity_utilization, sum_attendance, delta, delta1, delta2, delta3)[2]

col1.metric("Avg Nb of Guest Carried" , '{:,.0f}'.format(guest), delta=delta1)
col2.metric("Nb of Guest Carried / Adjusted Capacity" , '{:,.0f}%'.format(avg_adjust_capacity_utilization), delta=delta2)
col3.metric("" , '{:,.0f}%'.format(per_cap_adj))

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

average_capacity = filtered_df['CAPACITY'].mean()
average_adjust_capacity = filtered_df['ADJUST_CAPACITY'].mean()
average_capacity_diff = average_capacity - average_adjust_capacity
guest = filtered_df['GUEST_CARRIED'].mean()
capacity_available =  average_adjust_capacity/average_capacity*100

col4.metric("Avg Capacity / Avg Ajusted Capacity" , '{:,.0f}%'.format(capacity_available))

st.markdown("##")


if selected_attraction != "Select All":
    st.write(f"Dive into the data for: :green[**{selected_attraction}**]")
    # Display the data in a table for the selected attraction
    columns_to_select = ['WORK_DATE', 'CAPACITY', 'ADJUST_CAPACITY', 'NB_UNITS', 'NB_MAX_UNIT', 'GUEST_CARRIED','UP_TIME']
    sub_df = filtered_df[columns_to_select]
    sub_df['CAPACITY'] = sub_df['CAPACITY'].round(2)
    sub_df['WORK_DATE'] = pd.to_datetime(sub_df['WORK_DATE'])
    sub_df['WORK_DATE'] = sub_df['WORK_DATE'].dt.strftime('%Y-%m-%d')

    grouped = sub_df.groupby('WORK_DATE').mean()
    new_column_names = {'CAPACITY':'AVG Capacity', 'ADJUST_CAPACITY':'AVG Adjusted Capacity', 
                    'NB_UNITS':'AVG NB Units', 'NB_MAX_UNIT':'AVG NB MAX Unit',
                    'GUEST_CARRIED':'AVG Nb of Guest Carried', 'UP_TIME':'AVG Time Running (mns)' }
    grouped.rename(columns=new_column_names, inplace=True)


    n_rows = st.slider('Number of rows to display', min_value=1, max_value=len(grouped), value=5, step=1)
    st.dataframe(grouped.head(n_rows).style.highlight_max(color='#D8FAD9', axis=0).highlight_min(color = '#FAD8F9', axis=0), use_container_width=True)

    #st.table(grouped.head(n_rows))


