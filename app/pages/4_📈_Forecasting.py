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

# Load Data

