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
mode=st.multiselect("Choose the data to analyze it",option,key="modes")
st.session_state
but=st.button("Click it")
co1,col2=st.columns([4,1])
with col2:
    basemap=st.selesctbox("Choose the Base Map",options, index)
    types=st.selectbox("Types",["See All","Natural","Cultural","Mixed"], disabled= st.session_state.disable_type)
    Inscdate=st.slider("Choose the Year",Dateint,Dateend,disabled=st.session_state.disable_inscdate)
    chbox=st.checkbox("3-D Presentation",disabled=st.session_state.disable_chbox)
    
with col1:
    m=leafmap.Map(center=[40, -100], zoom=4)
    if but==True:
        if "Region" in st.session_state.modes:
            st.session_state.disable_chbox=False
            if "Catagory" in st.session_state.modes:
                st.session_state.disable_type=False
                if"Inscription Date" in st.session_state.modes:
                    st.session_state.disable_inscdate=False
                    st.write("A")
                else:
                    st.write("B")
            elif "Inscription Date" in st.session_state.modes:
                st.session_state.disable_inscdate=False
                st.write("C")
            else:
                st.write("D")
        elif "Catagory" in st.session_state.modes:
            st.session_state.disable_type=False
            if"Inscription Date" in st.session_state.modes:
                st.session_state.disable_inscdate=False
                st.write("E")
            else:
                st.write("F")
        elif "Inscription Date" in st.session_state.modes:
            st.session_state.disable_inscdate=False
            st.write("G")
        else:
            st.write("Nothing Found")
    else:
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        
