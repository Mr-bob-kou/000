import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt
import pydeck as pdk
import math
import pandas as pd

st.set_page_config(layout="wide",page_title="My World Herritage Website", page_icon="☘️")
st.title("Main")
st.session_state
data="https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/main/point.geojson"
if 'heritage1' not in st.session_state:
    st.session_state.heritage1 = gpd.read_file(data)

heritage=st.session_state.heritage1
regions = "https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/main/world-administrative-boundaries.geojson"
reg_df=gpd.read_file(regions)
#data2="https://github.com/Mr-bob-kou/My_Respository/raw/main/World%20Heritage%20Counts.geojson"
#Count=gpd.read_file(data2)
data3="https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/refs/heads/main/point2.geojson"
heritage2=gpd.read_file(data3)
heritage_sort=heritage.sort_values(by='NAME', ascending=True)
heritage_sort=heritage.sort_values(by='COUNTRY', ascending=True)

options = list(leafmap.basemaps.keys())
index = options.index("OpenStreetMap")
modes=["Default","Heat Map","Choropleth Map","Inscribed Date","Catagory"]
modes1="Default"
opt=["See All"]+list(heritage_sort['NAME'])
country=["See All"]+list(set(heritage_sort['COUNTRY']))

def Default(datum,mp,lon,lat,pop):
    mp.add_geojson(regions, layer_name="Countries",zoom_to_layer=False)
    mp.add_points_from_xy(datum,x=lon,y=lat, popup=pop)
    mp.add_basemap(basemap)
    return mp.to_streamlit(height=700)

def Info(NAME,COUNTRY,DESC):
    st.write("INFO:")
    st.write("Heritage Name:",NAME)
    st.write("Country:",COUNTRY)
    st.write("Description:",DESC)






with st.expander("See All Heritage Data"):
    st.dataframe(data=heritage, use_container_width=True)
col1, col2 = st.columns([4, 1])

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)
    country=st.selectbox("Choose a Country",country)
    
    place=st.selectbox("Choose a Place",opt)
    s=heritage[heritage['NAME']==place]
    if place=="See All":
        Info("NA","NA","NA")
    else:
        s=heritage[heritage['NAME']==place]
        h_name=s['NAME'].to_string(index=False)
        h_country=s['COUNTRY'].to_string(index=False)
        h_des=s['DESCRIPTIO'].to_string(index=False)
        Info(h_name,h_country,h_des)
            

with col1:
    m = leafmap.Map(center=[40, -100], zoom=4)
    if place=='See All':
        m1 = leafmap.Map(center=[0,0], zoom=1,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
        pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
        Default(heritage,m1, "LONGITUDE","LATITUDE",pop)
    else:
        lat=s['LATITUDE'].to_string(index=False)
        long=s['LONGITUDE'].to_string(index=False)
        centers=[lat,long]
        m7 = leafmap.Map(center=centers,zoom=15,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
        pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
        Default(heritage,m7, "LONGITUDE","LATITUDE",pop)

   
