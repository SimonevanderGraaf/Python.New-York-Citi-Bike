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
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'New York Citi Bike Strategy Dashboard', layout='wide')
st.title("New York Citi Bike Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Relation between bike usage and the weather",
   "Top 20 most popular start stations",
    "Interactive map showing popular bike trips", "Usage of bike types per average temperature", "Conclusion and recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('dualaxis.csv', index_col = 0)
top20 = pd.read_csv('top20NY.csv', index_col = 0)
small = pd.read_csv('reduced_data_to_plot_7.csv', index_col = 0)

# ######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### New York Citi Bike has been having distribution problems, which results in the increase of bike shortage at popular bike stations and therefore in the increase of customer complaints. This dashboard will help tackle these problems.")
    st.markdown("Right now, New York Citi bikes are often not available at popular stations at certain times. This analysis locates the details of these problems so a strategy can be created to solve them. The dashboard is separated into 5 parts:")
    st.markdown("- Relation between bike usage and the weather")
    st.markdown("- Top 20 most popular start stations")
    st.markdown("- Interactive map showing popular bike trips")
    st.markdown("- Usage of bike types per average temperature")
    st.markdown("- Conclusion and recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")   

    IntroImage = Image.open("citibike1.jpg") #source: https://unsplash.com/s/photos/citi-bike
    st.image(IntroImage)

    ### Create the dual axis line chart page ###
    
elif page == 'Relation between bike usage and the weather':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'steelblue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature (°C)', marker={'color': df['avgTemp'],'color': 'orange'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike rides and temperatures in 2022',
    height = 600
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("When looking at the dual axis line plot, it becomes clear there is a strong correlation between the daily temperatures and the daily bike rides. When temperatures rise, the number of daily bike rides increase as well. And when it is cold outside there are less people using a bike as transportation.") 
    st.markdown("This insight shows that the bike shortage problems probably occur in the warmer months in spring, summer and fall, from May to October.")

### Most popular bike stations page

    # Create the season variable

elif page == 'Top 20 most popular start stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=small['season'].unique(),
    default=small['season'].unique())

    df1 = small.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular start stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of bike rides',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Throughout the whole year there is a clear top 3 of popular start stations:") 
    st.markdown("Broadway & W 58 St, W 21 st & 6 Ave and West St & Chambers St. Followed closely by 6 Ave & W 33 St.")
    st.markdown("When looking specifically at the months in spring, summer and fall, there is a big difference in popularity between these 4 bike stations and the other 16 in the top 20.")

elif page == 'Interactive map showing popular bike trips': 

    ### Create the map ###

    st.write("Interactive map showing popular bike trips in New York")

    path_to_html = "NewYorkBikeTrips.html"

    # Read file and keep in variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    ## Show in web page 
    st.write("#### Aggregated bike rides in New York")
    st.components.v1.html(html_data,height = 1000)
    st.markdown("This interactive map shows the aggregated bike rides in the city. Visually it becomes quickly clear that most of the popular bike trips are alongside the waterfront and in Central Park. This explains why the most used start stations from the bar chart on the previous page are popular as they are great starting points of these touristic routes.")
   
elif page == 'Usage of bike types per average temperature': 
    
    ### Create a stacked bar chart ###
    # Filter data to be within the given temperature range
    filtered_df = small[(small['avgTemp'] >= -11.7) & (small['avgTemp'] <= 31.3)]

    # Group by avgTemp and rideable_type and calculate the sum of trips
    grouped_df = filtered_df.groupby(['avgTemp', 'bike_type'], as_index=False).agg({'value': 'sum'})

    # Pivot the data for the stacked bar chart
    pivot_df = grouped_df.pivot(index='avgTemp', columns='bike_type', values='value').fillna(0)

    # Create the stacked bar chart
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=pivot_df.index, y=pivot_df['electric_bike'], name='Electric Bike'))
    fig3.add_trace(go.Bar(x=pivot_df.index, y=pivot_df['classic_bike'], name='Classic Bike'))

    # Update layout for stacked bar chart
    fig3.update_layout(
    barmode='stack',
    title='Sum of bike rides by average temperature and bike type',
    xaxis_title='Average temperature (°C)',
    yaxis_title='Sum of bike rides',
    width=900, height=600
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('Comparing the use of classic bikes and electric bikes will show if both bike types need to be stored more frequently in order to avoid bike shortage.')
    st.markdown('The stacked bar chart shows that classic bikes are rented much more often. With very cold temperatures it happens often that the electric bikes are used as much as classic bikes, but the amount of bike rides during this period are very low.')
    st.markdown('In general, the use of electric bikes is between 25 and 35 percent of the total bike use. The amount of bike rides fluctuates a lot between the different temperatures for both bike types, mostly for the use of classic bikes as these are used a lot more often.')
                            
else:
    
    st.header("Conclusion and recommendations")
    st.markdown('#### Our analysis has shown that New York Citi Bike should focus on the following objectives moving forward:')
    st.markdown('- There is a strong correlation between temperatures and daily bike rides. I recommend New York Citi bike to increase the supply of bikes during the warmer months, from May to October. In the coldest months bikes are used a lot less frequently. To reduce costs, a lower availability in bikes during these months is advisable.')
    st.markdown('- The most popular start stations are at the waterfront and at Central Park. I recommend increasing the number of bikes at these stations and reviewing these areas for possibilities of adding extra bike stations.')
    st.markdown('- In the warmer and more popular months, electric bikes are used between 25 and 35 percent of the total bike use. As the rent of these bikes is more expensive, I would recommend exploring opportunities that will increase the use of electric bikes and therefore increase revenue.')

    bikesign = Image.open("Rec3.jpg")  #source: https://unsplash.com/s/photos/citi-bike
    st.image(bikesign)
