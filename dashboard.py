import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import plotly.io as pio





warnings.filterwarnings('ignore')
pio.renderers.default = 'browser'
st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

st.title(" 1st Vis")
st.header('What ius this')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


circuits= pd.read_csv('f1/circuits.csv')
circuits=circuits.drop(['circuitRef','name','alt','url'],axis=1)

fig = px.scatter_mapbox(circuits, lat="lat", lon="lng",
                        color_discrete_sequence=["fuchsia"], zoom=3, height=500, width=500)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
options = st.multiselect('Which continent would you like to see?', ['Asia', 'Europe','North America' ,'South America', 'Africa', 'Oceania'])

st.plotly_chart(fig)



st.title(" 2nd Vis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#for vis 2
options2 = st.multiselect('Time-Frame?', ['All-time', '2001-2010','2011-2020' ,'1991-2000'])


#for vis3
st.title(" 3rd Vis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


data = dict(
    character=["", "MOnza", "Tokyo", "MOntreal", "Miami", 'Sakhir','Singapore'],
    parent=["", "2013", "2014", "2015", "2016", "2017", "2018" ],
    value=[10, 14, 12, 10, 2, 6,8])

fig3 = px.sunburst(
    data,
    names='character',
    parents='parent',
    values='value',
)
st.plotly_chart(fig3)
