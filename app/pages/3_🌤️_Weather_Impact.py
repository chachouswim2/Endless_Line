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
