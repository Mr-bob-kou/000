import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import altair as alt
import ipyleaflet

st.set_page_config(layout="wide")

m=leafmap.Map()
st.title("Adding!!")
yr_range=list(range(1900,2100))
tp=["Natural","Cultural","Mixed"]
rg=list(set(st.session_state.heritage1["REGION"]))
tab1, tab2=st.tabs(["Add Heritage", "Delete Heritage"])
def bol_to_num(bol):
    if bol==True:
        num=1
    else:
        num=0
    return num
st.session_state
with tab1:
    with st.form("my_form"):
        name = st.text_input("Name")
        country= st.text_input("Country")
        region=st.selectbox("Region",rg)
        year=st.selectbox("Inscribed Year",yr_range)
        description=st.text_area("Description","NA")
        co1,co2=st.columns([1,1])
        with co1:
            x_cord=st.text_input("Longitude",0) 
            y_cord=st.text_input("Latitude",0)
            loct=[y_cord,x_cord]
            type=st.selectbox("Type",tp)
            danger = st.radio("Is this Heritage in Danger?", ["Yes", "No"],key="danger")
            areha=st.text_input("Area(ha)")
            tb=st.checkbox("Transboundary?",key="TB")
            
        with co2:
            m=leafmap.Map(center=loct,zoom=15)
            m.add_marker(loct)
            m.to_streamlit(width=500, height=500)
        submitted = st.form_submit_button("Submit")
    if submitted:
        num=bol_to_num(tb)
        df1={'NAME':[name],
            'COUNTRY':[country],
            'INSCRIBDATE':[year],
            'DESCRIPTIO':[description],
            'REGION':[region],
            'LONGITUDE':[float(x_cord)],
            'LATITUDE':[float(y_cord)],
            "TRANSBOUND ":[num]}
        gdf = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1['LONGITUDE'], df1['LATITUDE']))
        st.dataframe(data=gdf,use_container_width=True)
        st.session_state.heritage1=pd.concat([gdf,st.session_state.heritage1], axis=0, join='outer')
            
with tab2:
    st.dataframe(data=st.session_state.heritage1, use_container_width=True)
