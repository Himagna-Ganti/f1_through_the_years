


import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import plotly.io as pio
from streamlit_option_menu import option_menu

from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
import networkx as nx
import matplotlib.pyplot as plt


warnings.filterwarnings('ignore')
#pio.renderers.default = 'browser'
st.set_page_config(page_title="F1 through the years", page_icon=":bar_chart:",layout="wide")

opt= option_menu(menu_title=None,icons=['','',''],options=['HOME','AROUND THE WORLD IN 20 RACES','FASTEST FRONT-RUNNERS','GOAT', 'WHO-WHEN-WHERE'],orientation='horizontal',default_index=0,styles={"container":{"padding":"40px",'margin-top':'10px'}})



if opt=='HOME':
    st.markdown('# :red[F1 THROUGH THE YEARS]')
    st.markdown('---')
    st.markdown('##### This visualisation aims at extracting useful information from datasets pertaining to F1 races and displays them using various interactive various visualisations.  The reason this project exists is to show some key facts about F1 for anyone who needs immediate access to these stats. There are mainly 4 visualisations at the moment that are up and running in real time for you to explore.  ')
    st.markdown('##')
    st.markdown('#### Overview of the Dataset:')
    
    st.markdown('##### The dataset is a culmination of 14 csv files with various data fields. The main data fields that have been extracted and cleaned are Driver Names, Race Wins, Race track coordinates, LapTimings of different circuits, and Team names.   ')
    st.markdown('##')

    st.markdown('#### :red[AROUND THE WORLD IN 20 RACES:]')
    st.markdown('##### This visualisation tries to tell the story of the extreme logistics involved in F1, wherein there are races in 6 of the 7 continents every year spanning about 19-20 races which is where the name of the visualisation comes from. ')
    st.markdown('##')
    st.markdown('#### :red[FASTEST FRONT-RUNNERS:]')
    st.markdown('##### F1 is the pinnacle of motorsporting. The speeds touched by an F1 machine are like any other and the cars are only getting better and better. This visualisation shows you how the __fastest__ __lap__ __times__ of a particular race track has changed over the years.  ')
    st.markdown('##')
    st.markdown('#### :red[GOAT:]')
    st.markdown('##### Not just Greatest of all time but also Greatest of a specified time. This visualisation queries the number of wins secured by a particular driver in a given time period and displays the top 5 drivers of that time period.')
    st.markdown('##')
    st.markdown('#### :red[WHO-WHEN-WHERE:]')
    st.markdown('##### A quick way to get data on "who" won, "when" they won, and "where" they won a race. This visualisation queries the top 5 drivers who finished a race in particular year at a particular circuit. ')

    
    
elif opt=='AROUND THE WORLD IN 20 RACES':

    st.title("AROUND THE WORLD IN 20 RACES:")
    
    #st.markdown('##### This visualisation tries to tell the story of the extreme logistics involved in F1, wherein there are races in 6 of the 7 continents every year spanning about 19-20 races which is where the name of the visualisation comes from. ')
    st.markdown('### Tasks accomplished:')
    st.markdown('##### 1. Get an understanding of how F1 races are spread across the world.')
    st.markdown('##### 2. Explore the spread of F1 in a single continent with the countries they are being held in.')
    st.markdown('##### 3. Juxtapose more than one continent with another for understanding the contrast.')
    st.markdown('##### 4. Tooltip also displays the name of the circuit as well the country it is located in. ')
    st.markdown('##')
    st.markdown('### Instructions:')
    st.markdown('##### 1. The map is initially rendered with all the data points. .')
    st.markdown('##### 2. Select as many continents as you wish to compare. Atleast one continent needs to be selected.')
    st.markdown('##### 3. Double click on a title in the legend to highlight only the corresponding data points.')

    All_circuits= pd.read_csv('f1/circuits/all_circuits.csv')
    Europe= pd.read_csv('f1/circuits/europe.csv')
    Asia= pd.read_csv('f1/circuits/asia.csv')
    Oceania= pd.read_csv('f1/circuits/oceania.csv')
    Africa= pd.read_csv('f1/circuits/africa.csv')
    Americas= pd.read_csv('f1/circuits/americas.csv')
    dic={'Asia':Asia,'Europe':Europe,'Oceania':Oceania,'Africa':Africa,'Americas':Americas}
    left, middle, right = st.columns((2, 6, 2))
    with middle:
        selected = st.multiselect('', ['Asia', 'Europe','Americas', 'Africa', 'Oceania'],)

    if not selected:
        circuits=All_circuits
    else:
        circuit_df_array=[]
        for s in selected:
            circuit_df_array.append(dic[s])
        circuits=pd.concat(circuit_df_array)

    color_chart={'Asia':'#32F706','Oceania':'#06C8F7 ','Europe':'#F706F7','Americas':'#F70606','Africa':'#F7A006'}

    fig = px.scatter_mapbox(circuits, lat="lat", lon="lng",hover_name='country', hover_data={'name':True,'lat':False,'lng':False},color='continent',
                            color_discrete_map=color_chart, zoom=3, height=800, width=800,
        ).update_traces(marker={"size": 12,})
                            
    fig.update_layout(mapbox_style="open-street-map")

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},)
    fig.update_layout(showlegend=True,legend_font_size=30,font_size=10,height=500,width=800)
    fig.update_layout(hoverlabel=dict(
                bgcolor="white",
                font_size=18,
                font_color="black"
            ))
    
    left, middle, right = st.columns((2, 5, 2))
    with middle:
        st.plotly_chart(fig)

elif opt=='FASTEST FRONT-RUNNERS':
    #Second Visualisation will start here

    st.title("FASTEST FRONT-RUNNERS:")

    st.markdown('### Tasks accomplished:')
    st.markdown('##### 1. Compare the __fastest__ __lap__ __times__ of race track over the years.')
    st.markdown('##### 2. Each tooltip also displays information about the time in minutes, year it was set in, and name of the driver who set the fastest lap time.')
    st.markdown('##')
    st.markdown('### Instructions:')
    st.markdown('##### 1. To reduce compute load on the server while starting up, there is a :red[Load Data] button.')
    st.markdown('##### 2. Once the button is clicked the initial chart is rendered with the first datapoint in the csv file. You can choose atmost one race track to see its trend.')
  


    load= st.button('Load Data',key=1)

    if "load_state" not in st.session_state:
        st.session_state.load_state=False

    laptimes_drivers=pd.read_csv('f1/laptimes/laptimes_drivers.csv')


    if load or st.session_state.load_state:
        st.session_state.load_state=True
        left, middle, right = st.columns((1, 5, 1))
        with middle:
            chosen=st.radio(
                "Choose one Grand Prix",
                laptimes_drivers['name'].unique(),horizontal=True     
            )

        chosen=str(chosen)
        query = f"name == '{chosen}'"
        laptimes_drivers=laptimes_drivers.query(query)
        
        laptimes_drivers=laptimes_drivers.sort_values(by='year')
        fig = px.line(laptimes_drivers,x='year',y='stringTime',width=800, height=500,markers=True,hover_data={'fastestLapTime':True, 'stringTime':False,'FullName':True},)
        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=18,
                font_color="black"
            )   
        )
        fig.update_xaxes(
        
        title_text = "Year",
        title_font = {"size": 20},
        title_standoff = 25)

        fig.update_yaxes(
        title_text = "Fastest Lap Timings",
        title_font = {"size": 20},
        title_standoff = 25)


        fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                
                size=18,
                
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            tickfont=dict(
                
                size=18,
                
            ),
        ),)
        
        left, middle, right = st.columns((1, 5, 1))
        with middle:
            st.plotly_chart(fig)

elif opt=='GOAT':
    # 3rd Vis 

    st.title("GOAT:")

    st.markdown('### Tasks accomplished:')
    st.markdown('##### 1. Displays the top 5 drivers of a user-selected time period in the form of a bar-chart.')
    st.markdown('##### 2. Color of the barchart is color-coded to the team they were most successful in. ')


    st.markdown('##')
    st.markdown('### Instructions:')
    st.markdown('##### 1. To reduce compute load on the server while starting up, there is a :red[Load Data] button.')
    st.markdown('##### 2. Once the button is clicked the initial chart is rendered with the time-period set to All-time. This can be changed.')
    st.markdown('##### 3. Upon clicking Time-Range, a slider appears through which user can select a time-range they wish to visualise. ')
    st.markdown('##### 4. Upon clicking Year, a numeric input box appears where its min value is 2000 and max value is 2022 with a step increase of 1. Users can choose a particular year and its results. ')


    race_results=pd.read_csv('f1/wins/races_drivers.csv')
    drivers_with_colors=pd.read_csv('f1/wins/driver_names_with_colors.csv')
    race_results=race_results.sort_values(by='driverId')
    race_results=race_results.dropna()

    options=[]
    for i in range(2000,2023):
        options.append(i)
    load3= st.button('Load Data',key=2)

    if "load3_state" not in st.session_state:
        st.session_state.load3_state=False

    if load3 or st.session_state.load3_state:
        st.session_state.load3_state=True

        e,lt, rt,ee = st.columns((5,5,5, 5))
        with lt:
            driver_or_cosntructors=st.radio(
                " ",
                ['Drivers'],     
            )
        with rt:
            time=st.radio(
                "Choose One",
                ['All time','Time-Range','Year'],     
            )

        if time=='All time':
            for did in race_results['driverId'].unique():

                query=f'driverId=={did} & position=="1" '
                drivers_with_colors.at[did-1,'Wins']=race_results.query(query).shape[0]
                
                drivers_with_colors=drivers_with_colors.sort_values(by='Wins', ascending=False)
        
        elif time=='Year':
            yr=st.number_input(label='Type an year',min_value=1999,max_value=2022,value=2000,step=1)
            for did in race_results['driverId'].unique():

                query=f'driverId=={did} & position=="1" & year=={yr}'
                drivers_with_colors.at[did-1,'Wins']=race_results.query(query).shape[0]
                
                drivers_with_colors=drivers_with_colors.sort_values(by='Wins', ascending=False)
        else:
            options=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
            le,me,re=st.columns((2,24,2))
            with me:
                start,end=st.select_slider('Choose a range',options,value=(2000, 2001))
            yrs=[]
            for i in range(start,end+1):
                yrs.append(i)
            
            for did in race_results['driverId'].unique():

                query=f'driverId=={did} & position=="1" & year in {yrs} '
                drivers_with_colors.at[did-1,'Wins']=race_results.query(query).shape[0]
                
                drivers_with_colors=drivers_with_colors.sort_values(by='Wins', ascending=False)


        arr=[]
        for n in drivers_with_colors['hexcode'].head(5):
            arr.append('rgb('+str(n)+')')
        lul=['#648FFF', '#785EF0', '#DC267F', '#FE6100','#FFB000']
        fig = px.bar(drivers_with_colors.head(5), y='FullName', x='Wins',color="FullName",hover_data={'FullName':True,'Wins':True,'TeamName':True, 'driverId':False},color_discrete_sequence=lul)
        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=18,
                font_color="black"
            )   
        )
        fig.update_xaxes(
        
        title_text = "Wins",
        title_font = {"size": 20},
        title_standoff = 25)

        fig.update_yaxes(
        title_text = "Driver",
        title_font = {"size": 20},
        title_standoff = 25)
        fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                
                size=18,
                
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
            tickfont=dict(
                
                size=18,
                
            ),
        ),)
        fig.update_layout(legend = dict(font = dict( size = 18,)),
                  legend_title = dict(font = dict(size = 18)))
        left, middle, right = st.columns((5, 10, 5))
        with middle:
            st.plotly_chart(fig)







else:

    st.title("WHO-WHEN-WHERE:")

    st.markdown('### Tasks accomplished:')
    st.markdown('##### 1. Displays the top 5 drivers who finished a race at a particular circuit in a given year.')
    st.markdown('##### 2. There is a metric display of the Drivers, the teams they were racing for, and the position they secured in the race.')
    st.markdown('##')
    st.markdown('### Instructions:')
    st.markdown('##### 1. Select the year whose results you want to examine using the numeric input box. The minimum value is 2005 and the max value is 2022.')
    st.markdown('##### 2. Based on the rendered options in racetracks, select one to display the drivers who finished Top 5.')
  

    race_results=pd.read_csv('f1/fourth/fourth.csv')
    le,me,re=st.columns((10,10,10))
    with me:
        yr=st.number_input(label='Type an year',min_value=2005,max_value=2022,value=2005,step=1)
    
    filtered_df= race_results[race_results['year']==yr]
    left, middle, right = st.columns((1, 5, 1))
    with middle:
        chosen=st.radio(
            "Choose one Grand Prix",
            filtered_df['name'].unique(),horizontal=True     
        )
    further_df= filtered_df[filtered_df['name']==chosen]
    final_df=further_df[further_df['positionOrder']<=5]
    final_df = final_df.sort_values(by='positionOrder')
    

    fromm = []
    to=[]
    for index,row in final_df.iloc[1:5].iterrows():
        fromm.append(row['code'])

    for index,row in final_df.iloc[0:4].iterrows():
        to.append(row['code'])
    new_df= pd.DataFrame({'from': fromm, 'to': to})
    G=nx.from_pandas_edgelist(new_df, 'from', 'to')
    fig = plt.figure()
    nx.draw(G, with_labels=True, node_size=700, node_color="#FF1801",arrows=True,font_size=8,font_color="white",font_weight="bold", node_shape="o",edge_color='white', pos=nx.kamada_kawai_layout(G))
    fig.set_facecolor("#0E1117")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    left, middle, right = st.columns((15, 5, 10))
    with left:
        st.pyplot(fig)
    with right:
        x=0
        for index,row in final_df.iterrows():
            st.metric(label=row['team_name'], value=row['Full Name'], delta=x+1)
            x+=1
        