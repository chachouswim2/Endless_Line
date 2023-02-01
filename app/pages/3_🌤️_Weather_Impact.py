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
import altair as alt

import sys 
sys.path.append('../')
from features.build_data import * 
from features.streamlit_functions import *

st.set_page_config(layout="wide", page_title="Weather Impact", page_icon=":mostly_sunny:")

st.markdown("<h1 style='color:#5DB44C'>Impact of the Weather on E's activities</h1>", unsafe_allow_html=True)

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


######################### WEATHER ON ATTENDANCE AND WAIT TIME #################################

#Weather
weather = df['weather_description'].unique()
weather = ['Select All'] + list(weather)
selected_weather = st.selectbox('Select a weather:', weather)
if selected_weather != "Select All":
    filtered_df = df[df['weather_description'] == selected_weather]
else:
    filtered_df = df

#Metric
metric = list(['Attendance', 'Waiting Times'])
selected_metric = st.selectbox("Select what metric that you'd like to explore:", metric)

#Graph narrow down
view = list(['All', 'Yearly', 'Monthly', 'Daily'])
selected_view = st.selectbox("Select the scale to see the graph at:", view)

# Filter the df based on the selected filters
if selected_metric == "Attendance":
    if selected_view == 'Monthly':
        time_df = filtered_df.groupby("month")["attendance"].mean().reset_index()
        time_df['Month'] = time_df['month'].map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        chart = alt.Chart(time_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('month:O', title='Month'),
            y=alt.Y('attendance:Q', title='Avg Attendance')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='month:O',
            y='attendance:Q'
        )
        st.write(chart+line)

    elif selected_view == 'Daily':
        time_df = filtered_df.groupby("day")["attendance"].mean().reset_index()
        chart = alt.Chart(time_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('day:O', title='Day'),
            y=alt.Y('attendance:Q', title='Avg Attendance')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='day:O',
            y='attendance:Q'
        )
        st.write(chart+line)

    elif selected_view == 'Yearly':
        time_df = filtered_df.groupby("year")["attendance"].mean().reset_index()
        chart = alt.Chart(time_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('attendance:Q', title='Avg Attendance')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='year:O',
            y='attendance:Q'
        )
        st.write(chart+line)

    else:
        time_df = filtered_df.groupby("WORK_DATE")["attendance"].mean().reset_index()
        chart = alt.Chart(time_df).mark_line(color="#5DB44C").encode(
            x= alt.X('WORK_DATE', title="Date"),
            y=alt.Y('attendance', title='Attendance'),
        ).properties(
            title='Average Attendance over time', width=1250)
        st.write(chart)
elif selected_metric == "Waiting Times":
    if selected_view == 'Monthly':
        time_df = filtered_df.groupby("month")["WAIT_TIME_MAX"].mean().reset_index()
        time_df['Month'] = time_df['month'].map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        chart = alt.Chart(time_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('month:O', title='Month'),
            y=alt.Y('WAIT_TIME_MAX:Q', title='Avg Waiting Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='month:O',
            y='WAIT_TIME_MAX:Q'
        )
        st.write(chart+line)

    elif selected_view == 'Daily':
        time_df = filtered_df.groupby("day")["WAIT_TIME_MAX"].mean().reset_index()
        chart = alt.Chart(time_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('day:O', title='Day'),
            y=alt.Y('WAIT_TIME_MAX:Q', title='Avg Waiting Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='day:O',
            y='WAIT_TIME_MAX:Q'
        )
        st.write(chart+line)

    elif selected_view == 'Yearly':
        time_df = filtered_df.groupby("year")["WAIT_TIME_MAX"].mean().reset_index()
        chart = alt.Chart(time_df).mark_bar(color="#D8FAD9").encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('WAIT_TIME_MAX:Q', title='Avg Waiting Time')
        ).properties(
            width=1250
        )
        line = chart.mark_line(color='#5DB44C').encode(
            x='year:O',
            y='WAIT_TIME_MAX:Q'
        )
        st.write(chart+line)

    else:
        time_df = filtered_df.groupby("WORK_DATE")["WAIT_TIME_MAX"].mean().reset_index()
        chart = alt.Chart(time_df).mark_line(color="#5DB44C").encode(
            x= alt.X('WORK_DATE', title="Date"),
            y=alt.Y('WAIT_TIME_MAX', title='Waiting Time'),
        ).properties(
            title='Average Waiting Time over time', width=1250)
        st.write(chart)
