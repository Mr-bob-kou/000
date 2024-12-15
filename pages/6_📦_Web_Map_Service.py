import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt

st.set_page_config(layout="wide")


st.title("Adding!!")
yr_range=list(range(1900,2100))
tp=["Natural","Cultural","Mixed"] 
with st.form("my_form"):
    st.write("Inside the form")
    name = st.text_input("Name")
    country= st.text_input("Country")
    year=st.selectbox("Inscribed Year",yr_range)
    description=st.text_area("Description","NA")
    co1,co2=st.columns([1,1])
    with co1:
        x_cord=st.text_input("Longitude") 
        y_cord=st.text_input("Latitude")
        type=st.selectbox("Type",tp) 
        danger = st.radio("Is this Heritage in Danger?", ["Yes", "No"])
    with co2:
        m=leafmap.Map()
        m.to_streamlit(width=500, height=500)
    
    submitted = st.form_submit_button("Submit")
if submitted:
    st.write("Name", name, "Country", country)
    st.write("Year",year)
    st.write("description",description)
    st.write(x_cord)
