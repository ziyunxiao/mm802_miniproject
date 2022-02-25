# -*- coding: utf-8 -*-
from copyreg import pickle
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import pickle as pkl

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title='Find the good neighbourhood', layout = 'wide', initial_sidebar_state = 'auto')
# st.beta_set_page_config(page_title='Find the good neighbourhood', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')


# LOADING DATA
@st.experimental_memo
def load_data(fname):
    data = pkl.load(open(fname,'rb'))
    return data

data = load_data('./prop_crime.pkl')


# CREATING FUNCTION FOR MAPS
def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("Edmonton Housing Searching Tool")

with row1_2:
    st.write(
    """
    ##
    This project is make an assumption that someone who newly comes to the city of Edmonton. He/She is looking for a house. This tool will help them to find a house based on the neighbourhood and crimes.
    """)

# Q1
st.markdown("# Q1: Get top 10 neighborhood based on Average single house price")
price_range = st.slider( 'Select a range of values(x 1000)',  200, None, (300,600),step=10)
df1 = data.loc[(data['value']>=price_range[0] * 1000) & (data['value']<= price_range[1] * 1000),["neighbourhood","value"]]
st.write(price_range)
st.dataframe(df1)


# Q2
st.markdown("# Q2: Get top 10 neighborhood based single house price & crime occurances")
crime_num = st.slider( 'crime number no bigger than',  0, None, 10,step=1)
df2 = data.loc[(data['value']>=price_range[0] * 1000) & (data['value']<= price_range[1] * 1000 ) \
    & (data['crimes'] <=crime_num ),["neighbourhood","value","crimes"]]
st.write(crime_num)
st.dataframe(df2)

# Q3
st.markdown("# Q3: Overall consideration")
top_n = st.slider( 'show top N results',  1, 50, 5,step=1)
df3 = data.loc[(data['value']>=price_range[0] * 1000) & (data['value']<= price_range[1] * 1000 ) \
    & (data['crimes'] <=crime_num ),["neighbourhood","value","crimes"]]
df3['score'] = df3['crimes'] * 100000 / df3['value']
df3.sort_values(by = 'score',  ascending = False, inplace = True)
st.dataframe(df3.head(top_n))

