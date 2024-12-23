import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt
import pydeck as pdk
import math
import pandas as pd

st.set_page_config(layout="wide")

st.title("Analysis")
option=["Region","Catagory","Inscription Date"]
mode=st.multiselect("Choose the data to analyze it",option,key="modes")
st.session_state
but=st.button("Click it")
if but==True:
    if "Region" in st.session_state.modes:
        if "Catagory" in st.session_state.modes:
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
        st.write("H")
        
