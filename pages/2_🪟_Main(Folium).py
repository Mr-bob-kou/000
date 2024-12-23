import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt
import pydeck as pdk
import math
import pandas as pd

st.set_page_config(layout="wide")

heritage=st.session_state.heritage1

regions = "https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/main/world-administrative-boundaries.geojson"
reg_df=gpd.read_file(regions)
Dateint=heritage['DATEINSCRI'].min()
Dateend=heritage['DATEINSCRI'].max()
bas_options = list(leafmap.basemaps.keys())
index = bas_options.index("OpenStreetMap")

if "disable_type" not in st.session_state:
    st.session_state.disable_type=True
    st.session_state.disable_inscdate=True
    st.session_state.disable_chbox=True

st.title("Analysis")
option=["Region","Catagory","Inscription Date"]
st.session_state
col3,col4=st.columns([4,1])
with col3:
    mode=st.multiselect("Choose the data to analyze it",option,key="modes")
with col4:
    but=st.button("Click it")
col1,col2=st.columns([4,1])
if st.button("Rerun"):
    st.rerun()
with col2:
    basemap=st.selectbox("Choose the Base Map",bas_options, index)
    if "Region" in st.session_state.modes:
        types=st.selectbox("Types",["See All","Natural","Cultural","Mixed"])
    if "Catagory" in st.session_state.modes:
        Inscdate=st.slider("Choose the Year",Dateint,Dateend)
    if "Inscription Date" in st.session_state.modes:    
        chbox=st.checkbox("3-D Presentation",disabled=st.session_state.disable_chbox)
    
with col1:
    m=leafmap.Map(center=[40, -100], zoom=4)
    if but==True:
        if "Region" in st.session_state.modes:
            if "Catagory" in st.session_state.modes:
                chbox=st.checkbox("3-D Presentation")
                if"Inscription Date" in st.session_state.modes:
                    st.write("A")
                else:
                    st.write("B")
            elif "Inscription Date" in st.session_state.modes:
                st.write("C")
            else:
                st.write("D")
        elif "Catagory" in st.session_state.modes:
            if"Inscription Date" in st.session_state.modes:
                st.write("E")
            else:
                st.write("F")
        elif "Inscription Date" in st.session_state.modes:
            st.write("G")
        else:
            st.write("Nothing Found")
    else:
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        
