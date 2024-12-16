import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt
import ipyleaflet

st.set_page_config(layout="wide")

m=leafmap.Map()
st.title("Adding!!")
yr_range=list(range(1900,2100))
tp=["Natural","Cultural","Mixed"]
tab1, tab2=st.tabs(["Add Heritage", "Delete Heritage"])
st.session_state
m1=leafmap.Map(center=[0,0],zoom=7)
m1.to_streamlit(width=500, height=500,key="map")
with tab1:
    with st.form("my_form"):
        st.write("Inside the form")
        name = st.text_input("Name")
        country= st.text_input("Country")
        year=st.selectbox("Inscribed Year",yr_range)
        description=st.text_area("Description","NA")
        co1,co2=st.columns([1,1])
        with co1:
            x_cord=st.text_input("Longitude",0) 
            y_cord=st.text_input("Latitude",0)
            loct=[y_cord,x_cord]
            type=st.selectbox("Type",tp) 
            danger = st.radio("Is this Heritage in Danger?", ["Yes", "No"])
            areha=st.text_input("Area(ha)")
        with co2:
            m=leafmap.Map(center=loct,zoom=15)
            m.add_marker(loct)
            m.to_streamlit(width=500, height=500)
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Name", name, "Country", country)
        st.write("Year",year)
        st.write("description",description)
        st.write(x_cord)
