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

if "button_click" not in st.session_state:
    st.session_state.button_click=False

def to_df(datum,val):
    couda=datum.groupby(val).size()
    couda.to_frame()
    return couda.reset_index()

def type(name,color,type_name,color_code,pop):
    typee=heritage[heritage["CATSHORT"]==name]
    m.add_points_from_xy(typee,x="LONGITUDE",y="LATITUDE", popup=pop,color_column='CATSHORT',marker_colors=[color],icon_colors=[color],add_legend=False)
    legend_dict={type_name:color_code}
    m.add_legend(title="Classification", legend_dict=legend_dict, draggable=False)

def button_to_true():
    st.session_state.button_click==True
    



st.title("Analysis")
option=["Region","Catagory","Inscription Date"]
st.session_state
col3,col4=st.columns([4,1],vertical_alignment="bottom")
with col3:
    mode=st.multiselect("Choose the data to analyze it",option,key="modes")
with col4:
    but=st.button("Click it",key="bot")

col1,col2=st.columns([4,1])
if st.button("Rerun"):
    st.session_state.button_click=False
    st.rerun()
    


with col2:
    basemap=st.selectbox("Choose the Base Map",bas_options, index)
    if "Region" in st.session_state.modes:
        chbox=st.checkbox("3-D Presentation",disabled=st.session_state.disable_chbox)
    if "Inscription Date" in st.session_state.modes:    
        Inscdate=st.slider("Choose the Year",Dateint,Dateend)
    
with col1:
    m=leafmap.Map(center=[40, -100], zoom=4)
    if but==True or st.session_state.button_click:
        st.session_state.button_click=True
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
                with col2:
                    types=st.selectbox("Types",["See All","Natural","Cultural","Mixed"])
                pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
                m=leafmap.Map(center=[40, -100], zoom=4)
                m.add_geojson(regions, layer_name="Countries",zoom_to_layer=False)
                ct_group=to_df(heritage,"CATSHORT")
                ct_group.rename(columns={0:'count'},inplace=True)
                df_group=pd.DataFrame({"Types":["Cultural","Mixed","Natural"]})
                ct_group=pd.concat([ct_group,df_group],axis=1)
                ct_group_sort=ct_group.sort_value(by='count', ascending=True)
                if types=="See All":
                    m.add_points_from_xy(heritage,x="LONGITUDE",y="LATITUDE", popup=pop,color_column='CATSHORT',marker_colors=['orange','green','red'],icon_colors=['white','green','red'],add_legend=False)
                    legend_dict={"Cultural":"#FF8000",
                                 "Natural":"#008000",
                                 "Mixed":"#ff0000"}
                    m.add_legend(title="Classification", legend_dict=legend_dict, draggable=False)
                elif types=="Natural":
                    type("N",'green',"Natural","#008000",pop)
                elif types=="Cultural":
                    type("C","orange","Cultural","#FF8000",pop)
                elif types=="Mixed":
                    type("C/N","red","Mixed","#ff0000",pop)
                m.add_basemap(basemap)
                m.to_streamlit(height=700)
                if types=="See All":
                    charts_cat = alt.Chart(ct_group_sort).mark_bar(size=10).encode(x=alt.X("Types",type='nominal'),y=alt.Y("count",type="quantitative"))
                else:
                    cond=alt.condition(alt.datum.Types==types,alt.value('red'),alt.value('steelblue'))
                    charts_cat = alt.Chart(ct_group_sort).mark_bar(size=50).encode(x=alt.X("Types",type='nominal'),y=alt.Y("count",type="quantitative"),color=cond)
                pie=alt.Chart(ct_group).mark_arc().encode(theta="count",color="Types")
                col5,col6=st.columns([1,1])
                with col6:
                    se_box=st.selectbox("Select a Chart",["Bar Chart","Pie Chart"])
                with col5:
                    if se_box=="Bar Chart":
                        st.write("##Bar Chart")
                        st.altair_chart(charts_cat)
                    elif se_box=="Pie Chart":
                        st.write("##Pie Chart")
                        st.altair_chart(pie)
        elif "Inscription Date" in st.session_state.modes:
            st.write("G")
        else:
            st.write("Nothing Found")
    else:
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        
