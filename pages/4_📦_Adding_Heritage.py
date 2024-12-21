import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import altair as alt
import ipyleaflet
import time
from collections import OrderedDict

st.set_page_config(layout="wide")
datum=st.session_state.heritage1
rg_sort=st.session_state.heritage1.sort_values(by='REGION', ascending=True)

m=leafmap.Map()
st.title("Adding!!")
yr_range=list(range(1900,2100))
tp=["Natural","Cultural","Mixed"]
times=["Zero","One","Two","Three","Four","Five+"]
rg=list(OrderedDict.fromkeys(rg_sort["REGION"]))

def bol_to_num(bol):
    if bol==True:
        num=1
    else:
        num=0
    return num

def final_ct(a,b):
    if st.session_state.danger=="Yes":
        cat_fin=a
    else:
        cat_fin=b
    return cat_fin


tab1, tab2,tab3=st.tabs(["Add Heritage", "Edit Heritage","Delete Heritage"])
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
            st.write("Advanced:")
            just=st.text_area("Justification")
            revbis=st.radio("How many time is the data revised ",times,horizontal=True,key="time")
            
            
        with co2:
            m=leafmap.Map(center=loct,zoom=15)
            m.add_marker(loct)
            m.to_streamlit(width=500, height=500)
        submitted = st.form_submit_button("Submit")
    if submitted:
        num=bol_to_num(tb)
        if type=='Natural':
            cat_short="N"
            if st.session_state.danger=="Yes":
                cat_fin="ND"
            else:
                cat_fin="N"
        elif type=='Cutural':
            cat_short=='C'
            if st.session_state.danger=="Yes":
                cat_fin="CD"
            else:
                cat_fin="C"
        elif type=='Mixed':
            cat_short=='C/N'
        df1={'UNIQUENUM':[datum['UNIQUENUM'].max()+1],
            'IDNUM':[datum['IDNUM'].max()+1],
            'NAME':[name],
            'COUNTRY':[country],
            'LONGITUDE':[float(x_cord)],
            'LATITUDE':[float(y_cord)],
            'DATEINSCRI':[year],
            'DESCRIPTIO':[description],
            'REGION':[region],
            'CATSHORT':[cat_short],
            'CATFIN':[cat_fin],
            "TRANSBOUND":[num]}
        st.write(cat_fin)
        #gdf = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1['LONGITUDE'], df1['LATITUDE']))
        #st.dataframe(data=gdf,use_container_width=True)
        #st.session_state.heritage1=pd.concat([st.session_state.heritage1,gdf], axis=0, join='outer',ignore_index=True)
        #time.sleep(5)
        #st.rerun()
            
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
    row_name = st.selectbox("Select a row to delete:", st.session_state.heritage1['NAME'])
    id= st.session_state.heritage1[st.session_state.heritage1['NAME'] == row_name].index
    #index=id.to_string(index=False)
    st.write(id)
    button3=st.button("Delete the Row")
    if button3:
        st.session_state.heritage1=st.session_state.heritage1.drop(id)
        st.write("Wait 3 minetue")
        time.sleep(3)
        st.rerun()
    

    
