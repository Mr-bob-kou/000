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

def button_to_true():
    st.session_state.button_click==True

def form_type(data):
    ct_group=to_df(data,"CATSHORT")
    ct_group.rename(columns={0:'count'},inplace=True)
    df_group=pd.DataFrame({"Types":["Cultural","Mixed","Natural"]})
    ct_group=pd.concat([ct_group,df_group],axis=1)
    return ct_group

def color_marker(data):
    value=list(set(data["CATSHORT"]))
    if 'N' in value:
        if 'C' in value:
            if 'C/N' in value:
                color_map=['orange','green','red']
            else:
                color_map=['orange','green']
        else:
            color_map=['green']
    elif 'C' in value:
        if 'C/N' in value:
            color_map=['orange','red']
        else:
            color_map=['orange']
    elif 'C/N' in value:
        color_map=['red']
    else:
        color_map= None
    return color_map

def type(name,type_name,color_code,pop,data=heritage):
    typee=data[data["CATSHORT"]==name]
    color=color_marker(typee)
    if typee.empty:
        legend_dict={type_name:color_code}
        m.add_legend(title="Classification", legend_dict=legend_dict, draggable=False)
    else:
        m.add_points_from_xy(typee,x="LONGITUDE",y="LATITUDE", popup=pop,color_column='CATSHORT',marker_colors=color,icon_colors=color,add_legend=False)
        legend_dict={type_name:color_code}
        m.add_legend(title="Classification", legend_dict=legend_dict, draggable=False)

            
        
            
    
    



st.title("Analysis")
option=["Region","Category","Inscription Date"]
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
        chbox=st.checkbox("3-D Presentation")
    if "Category" in st.session_state.modes:
         types=st.selectbox("Types",["See All","Natural","Cultural","Mixed"])
    if "Inscription Date" in st.session_state.modes:    
        Inscdate=st.slider("Choose the Year",Dateint,Dateend)
    
with col1:
    m=leafmap.Map(center=[40, -100], zoom=4)
    if but==True or st.session_state.button_click:
        st.session_state.button_click=True
        if "Region" in st.session_state.modes:
            if "Category" in st.session_state.modes:
                if"Inscription Date" in st.session_state.modes:
                    st.write("A")
                else:
                    st.write("B")
            elif "Inscription Date" in st.session_state.modes:
                st.write("C")
            else:
                st.write("D")
        elif "Category" in st.session_state.modes:
            pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
            m=leafmap.Map(center=[40, -100], zoom=4)
            m.add_geojson(regions, layer_name="Countries",zoom_to_layer=False)
            if"Inscription Date" in st.session_state.modes:
                Cate_data=heritage[heritage['DATEINSCRI']==Inscdate]
                time_ct_group=form_type(Cate_data)
                cm=color_marker(Cate_data)
                st.write(Cate_data)
                if types=="See All":
                    m.add_points_from_xy(Cate_data,x="LONGITUDE",y="LATITUDE", popup=pop,color_column='CATSHORT',marker_colors=cm,icon_colors=cm,add_legend=False)
                    legend_dict={"Cultural":"#FF8000",
                                 "Natural":"#008000",
                                 "Mixed":"#ff0000"}
                    m.add_legend(title="Classification", legend_dict=legend_dict, draggable=False)
                elif types=="Natural":
                    type("N","Natural","#008000",pop,data=Cate_data)
                elif types=="Cultural":
                    type("C","Cultural","#FF8000",pop,data=Cate_data)
                elif types=="Mixed":
                    type("C/N","Mixed","#ff0000",pop,data=Cate_data)
                m.add_basemap(basemap)
                m.to_streamlit(height=700)
                st.write(time_ct_group)
            else:
                ct_group=to_df(heritage,"CATSHORT")
                ct_group.rename(columns={0:'count'},inplace=True)
                df_group=pd.DataFrame({"Types":["Cultural","Mixed","Natural"]})
                ct_group=pd.concat([ct_group,df_group],axis=1)
                if types=="See All":
                    m.add_points_from_xy(heritage,x="LONGITUDE",y="LATITUDE", popup=pop,color_column='CATSHORT',marker_colors=['orange','green','red'],icon_colors=['white','green','red'],add_legend=False)
                    legend_dict={"Cultural":"#FF8000",
                                 "Natural":"#008000",
                                 "Mixed":"#ff0000"}
                    m.add_legend(title="Classification", legend_dict=legend_dict, draggable=False)
                elif types=="Natural":
                    type("N","Natural","#008000",pop)
                elif types=="Cultural":
                    type("C","Cultural","#FF8000",pop)
                elif types=="Mixed":
                    type("C/N","Mixed","#ff0000",pop)
                m.add_basemap(basemap)
                m.to_streamlit(height=700)
                if types=="See All":
                    charts_cat = alt.Chart(ct_group).mark_bar(size=20).encode(x=alt.X("Types",type='nominal').sort("y"),y=alt.Y("count",type="quantitative"))
                else:
                    cond=alt.condition(alt.datum.Types==types,alt.value('red'),alt.value('steelblue'))
                    charts_cat = alt.Chart(ct_group).mark_bar(size=20).encode(x=alt.X("Types",type='nominal').sort("y"),y=alt.Y("count",type="quantitative"),color=cond)
                pie=alt.Chart(ct_group).mark_arc().encode(theta="count",color="Types")
                col5,col6=st.columns([1,1])
                with col6:
                    se_box=st.selectbox("Select a Chart",["Bar Chart","Pie Chart"])
                with col5:
                    if se_box=="Bar Chart":
                        st.write("#### Bar Chart")
                        st.altair_chart(charts_cat,use_container_width=True)
                    elif se_box=="Pie Chart":
                        st.write("#### Pie Chart")
                        st.altair_chart(pie)
        elif "Inscription Date" in st.session_state.modes:
            st.write("G")
        else:
            st.write("Nothing Found")
    else:
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        
