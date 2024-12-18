import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import altair as alt
import ipyleaflet
import time

st.set_page_config(layout="wide")
ct_sort=st.session_state.heritage1.sort_values(by='COUNTRY', ascending=True)
rg_sort=st.session_state.heritage1.sort_values(by='COUNTRY', ascending=True)
m=leafmap.Map()
st.title("Adding!!")
yr_range=list(range(1900,2100))
tp=["Natural","Cultural","Mixed"]
rg=list(set(rg_sort["REGION"]))
cout=list(set(ct_sort["COUNTRY"]))
tab1, tab2,tab3=st.tabs(["Add Heritage", "Edit Heritage","Delete Heritage"])
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
        country= st.selectbox("Country",cout)
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
            'DATEINSCRI':[year],
            'DESCRIPTIO':[description],
            'REGION':[region],
            'LONGITUDE':[float(x_cord)],
            'LATITUDE':[float(y_cord)],
            "TRANSBOUND":[num]}
        gdf = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1['LONGITUDE'], df1['LATITUDE']))
        st.dataframe(data=gdf,use_container_width=True)
        st.session_state.heritage1=pd.concat([gdf,st.session_state.heritage1], axis=0, join='outer')
        time.sleep(5)
        st.rerun()
            
with tab2:
    edit_df=st.data_editor(st.session_state.heritage1, use_container_width=True,num_rows="dynamic")
    but2=st.button("Update")
    if but2==True:
        if not edit_df.equals(st.session_state.heritage1):
            st.session_state.heritage1=edit_df
            st.write("Updated_Sucessfully")
            time.sleep(3)
            st.rerun()
with tab3:
    st.dataframe(data=st.session_state.heritage1, use_container_width=True)
    row_index = st.selectbox("Select a row to delete:", st.session_state.heritage1['NAME'])

    
