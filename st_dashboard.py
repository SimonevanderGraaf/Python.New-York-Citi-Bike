################################################ NEW YORK CITY BIKE DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'New York Citi Bike Strategy Dashboard', layout='wide')
st.title("New York Citi Bike Strategy Dashboard")
st.markdown("New York Citi Bike has been having distribution problems which results in the increase of customer complaints. The dashboard will help tackle these problems.")
st.markdown("Right now, New York Citi bikes are often not available at popular stations at certain times. This analysis locates the details of these problems so a strategy can be created to solve them.")

########################## Import data ###########################################################################################

df = pd.read_csv('dualaxis.csv', index_col = 0)
top20 = pd.read_csv('top20NY.csv', index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'matter'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 700
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'purple'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'orange'}),
secondary_y=True
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###
path_to_html = "NewYorkBikeTrips.html"

# Read file and keep in variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()

## Show in web page 
st.write("#### Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height = 1000)