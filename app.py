# -*- coding: utf-8 -*-
from copyreg import pickle
from matplotlib.pyplot import show, title
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import pickle as pkl
import bokeh.plotting as bokplt

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(page_title='Find a good neighbourhood to live at Edmonton', layout = 'wide', initial_sidebar_state = 'auto')
# st.beta_set_page_config(page_title='Find the good neighbourhood', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')


# LOADING DATA
@st.experimental_memo
def load_data(fname):
    data = pkl.load(open(fname,'rb'))
    return data

data = load_data('./prop_crime.pkl')



# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("Edmonton Housing Searching Tool")

with row1_2:
    st.write(
    """
    ##
    This project is based on an assumption that someone who newly comes to the city of Edmonton. 
    He/She is looking for a house. This tool will help them to find a house based on the average price of single house and crimes for a neighbourhood.
    """)

# Q1
st.markdown("# Q1: Get top 10 neighborhood based on your budget")
price_range = st.slider( 'Select a range of values(x 1000)',  200, 2000, (300,600),step=10)
df1 = data.loc[(data['value']>=price_range[0] * 1000) & (data['value']<= price_range[1] * 1000),["neighbourhood","value"]]
st.write(price_range)
st.dataframe(df1)


# Q2
def show_q2():
    df2 = data.loc[(data['value']>=price_range[0] * 1000) & (data['value']<= price_range[1] * 1000 ) \
        & (data['crimes'] <=crime_num ),["neighbourhood","value","crimes"]]
    return df2

st.markdown("# Q2: Get top 10 neighborhood that has less crimes")
crime_num = st.slider( 'crime number no bigger than',  0, None, 10,step=1,on_change=show_q2)
st.write(crime_num)
df2 = show_q2()
st.dataframe(df2)

    # c = alt.Chart(df2).mark_line().encode(
    #     x='neighbourhood', y='value', tooltip=['neighbourhood', 'value'])
    # # st.altair_chart(c)
    # p = bokplt.figure(
    #     title='simple line example',
    #     x_axis_label='x',
    #     y_axis_label='y')
    # p.line(df2["neighbourhood"],df2["value"])
    # st.bokeh_chart(p)

# Q3
st.markdown("# Q3: Overall Sorting by price and crimes.")
st.markdown("")
top_n = st.slider( 'show top N results',  1, 50, 5,step=1)
df3 = data.loc[(data['value']>=price_range[0] * 1000) & (data['value']<= price_range[1] * 1000 ) \
    ,["neighbourhood","value","crimes","lat","lon"]]
df3['score'] =  df3['value']/ df3['crimes']
df3.sort_values(by = 'score',  ascending = False, inplace = True)
st.table(df3.head(top_n))

# show Neighbour on map
st.markdown("# Show Neighbour on map")

# CREATING FUNCTION FOR MAPS
# https://pydeck.gl/layer.html
# 
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
                "GridCellLayer",
                data=data,
                get_position=["lon", "lat"],
                get_elevation=["value"],
                get_fill_color=[180, 0, ["value"], 140],
                radius=100,
                elevation_scale=10,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

df4 = df3.drop(['value','crimes'],axis = 1)
df4["value"] = 255 * df4['score'] / (np.max(df4['score'])  - np.min(df4['score']))
# st.dataframe(df4)
df4 = df4.head(top_n)
edm = [53.5461, -113.4938]
map(df4, edm[0], edm[1], 11)