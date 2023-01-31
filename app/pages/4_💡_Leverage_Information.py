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
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


st.set_page_config(layout="wide", page_title="Leverage Information", page_icon=":flag:")
st.markdown("<h1 style='color:#5DB44C'>Leverage Information and optimize KPIs</h1>", unsafe_allow_html=True)
