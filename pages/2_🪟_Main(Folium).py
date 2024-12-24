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

if "disable" not in st.session_state:
    st.session_state.disable=False
    
if "Count10" not in st.session_state:
    st.session_state.Count10=None
if Count not in not in st.session_state:
    st.session_state.Count=None


legend_dict = {
    "0":'#FFFFFF',
    "0-10":'#D2E9FF',
    "10-20":'#ACD6FF',
    "20-30": '#46A3FF',
    "30-40": '#0066CC',
    "40+": '#003060',
}

legend_dict1 = {
    "0":'#FFFFFF',
    "0-3":'#D2E9FF',
    "3-7": '#46A3FF',
    "7-10": '#0066CC',
    "10+": '#003060',
}

COLOR_RANGE = [
    [255, 255, 255],
    [210, 233, 255],
    [172, 214, 255],
    [70, 163, 255],
    [0, 102, 204],
    [0, 48, 96]
]
BREAKS = [0,10,20,30,40,50]

COLOR_RANGE1 = [
    [255, 255, 255],
    [210, 233, 255],
    [70, 163, 255],
    [0, 102, 204],
    [0, 48, 96]
]
BREAKS1 = [0,3,7,10,20]


def style_function(feature):
    count = feature['properties']['count']
    
    if count > 40:
        color = '#003060'
    elif count > 30:
        color = "#0066CC"
    elif count > 20:
        color = '#46A3FF'
    elif count > 10:
        color = '#ACD6FF'
    elif count > 0 :
        color = '#D2E9FF'
    else:
        color='#FFFFFF'
    
    return {
        'fillColor': color,
        'color':"black",
        'weight': 2,
        'fillOpacity': 1
    }

def style_function1(feature):
    count = feature['properties']['count']
    
    if count > 10:
        color = '#003060'
    elif count > 7:
        color = "#0066CC"
    elif count > 3:
        color = '#46A3FF'
    elif count > 0:
        color = '#D2E9FF'
    elif count == 0 :
        color = '#FFFFFF'
    
    return {
        'fillColor': color,
        'color':"black",
        'weight': 2,
        'fillOpacity': 1
    }

def color_scale(val):
    for i, b in enumerate(BREAKS):
        if val <= b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]

def color_scale1(val):
    for i, b in enumerate(BREAKS1):
        if val <= b:
            return COLOR_RANGE1[i]
    return COLOR_RANGE1[i]


def calculate_elevation(val):
    return math.sqrt(val) * 20000

def cuml(datum,val):
    datum['aggr']=0
    for i in datum.index:
        if i==0:
            datum['aggr'][i]=datum[val][i]
        else:
            datum['aggr'][i]=datum[val][i]+datum['aggr'][i-1]
    return datum

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

def muti_chart(data,column,color):
    cond=alt.condition(alt.datum.DATEINSCRI==Inscdate,alt.value('red'),alt.value(color))
    point_chart=alt.Chart(data).mark_point(filled=True,opacity=1).encode(x=alt.X("DATEINSCRI", type='temporal'),y=alt.Y(column, type="quantitative"),color=cond)
    line_chart = alt.Chart(data).mark_line().encode(x=alt.X("DATEINSCRI",type='temporal'),
                                                                 y=alt.Y(column,type='quantitative',title='count'),
                                                                 color=alt.value(color))
    chart1=point_chart+line_chart
    return chart1

def count_sj(data,regions,colum="CATSHORT",cat=None):
    if cat==None:
        data1=data
    else:
        data1=data[data[colum]==cat]
    count=gpd.sjoin(data1,regions, how='inner', predicate='within')
    a=count.groupby("name").size()
    count_per_polygon = a.rename('count')
    count=pd.merge(regions, count_per_polygon,how='outer',left_on='name', right_index=True).fillna(0)
    return count.to_json()

def td_counter(data):
     deck=pdk.Deck(map_style="light",
            initial_view_state={
                "latitude": 0,
                "longitude": 0,
                "zoom":0,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "GeoJsonLayer",
                    data,
                    id="geojson",
                    opacity=0.8,
                    stroked=True,
                    get_fill_color="filled_color",
                    get_polygon="geometry",
                    get_elevation='elevation',
                    filled=True,
                    extruded=True,
                    wireframe=True,
                    pickable=True
                ),
            ],
        )
     return st.write(deck)

def chromap(datum,mp,style_function,ld):
    mp.add_basemap(basemap)
    mp.add_geojson(datum,style_callback=style_function) 
    mp.add_legend(title="Heritage Counts", legend_dict=ld,draggable=False,position="bottomright")
    return mp.to_streamlit(height=700)

def cat_crmap(data1,data2,style_function,legend_dict,color_scale,colum="CATSHORT",cat=None):
    data3=count_sj(data1,data2,colum=colum,cat=cat)
    Count=gpd.read_file(data3)
    count10=Count.sort_values(by='count', ascending=False).head(10)
    st.session_state.Count10=count10
    st.session_state_Count=Count
    Count["elevation"] = Count['count'].apply(calculate_elevation)
    Count["filled_color"]=Count['count'].apply(color_scale)
    if chbox:
        td_counter(Count)
    else:
        chromap(data3,m,style_function,legend_dict) 

            
        
            
    
    



st.title("Analysis")
option=["Region","Category","Inscription Date"]
st.session_state
col3,col4=st.columns([4,1],vertical_alignment="bottom")
with col3:
    mode=st.multiselect("Choose the data to analyze it",option,key="modes",disabled=st.session_state.disable)
with col4:
    but=st.button("Click it",key="bot")

col1,col2=st.columns([4,1])
if st.button("Rerun"):
    st.session_state.button_click=False
    st.session_state.disable=False
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
        st.session_state.disable=True
        st.session_state.disable=True
        if "Region" in st.session_state.modes:
            if "Category" in st.session_state.modes:
                if"Inscription Date" in st.session_state.modes:
                    st.write("A")
                else:
                    if types=='See All':
                        cat_crmap(heritage,reg_df,style_function,legend_dict,color_scale,cat=None) 
                    elif types=='Natural':
                        cat_crmap(heritage,reg_df,style_function1,legend_dict1,color_scale1,cat='N')
                    elif types=='Cultural':
                        cat_crmap(heritage,reg_df,style_function,legend_dict,color_scale,cat='C')
                    elif types=='Mixed':
                        cat_crmap(heritage,reg_df,style_function1,legend_dict1,color_scale1,cat='C/N')
            elif "Inscription Date" in st.session_state.modes:
                cat_crmap(heritage,reg_df,style_function1,legend_dict1,color_scale1,colum='DATEINSCRI',cat=Inscdate)
            else:
                cat_crmap(heritage,reg_df,style_function,legend_dict,color_scale,cat=None)
                col10,col11=st.columns([2,2])
                with col11:
                    charts_select=st.selectbox("Choose the Plot",["Bar Chart(Top 10)","Bar Chart","Pie Chart"])
                with coll0: 
                    pie=alt.Chart(st.session_state_Count).mark_arc().encode(theta="count",color="name")
                    charts = alt.Chart(st.session_state_count10).mark_bar(size=20).encode(x=alt.X("name",type="nominal").sort("y"),y=alt.Y("count",type="quantitative"))
                    bar_charts = alt.Chart(st.session_state_Count).mark_bar(size=20).encode(x=alt.X("name",type="nominal").sort("y"),y=alt.Y("count",type="quantitative"))
                    if charts_select=="Bar Chart(Top 10)":
                        st.write("#### Heritage Count Statistics(Top 10)")
                        st.altair_chart(charts,use_container_width=True)
                    if charts_select=="Bar Chart":
                        st.write("#### Heritage Count Statistics")
                        st.altair_chart(bar_charts,use_container_width=True)
                    elif charts_select=="Pie Chart":
                        st.write("#### Heritage Count Pie Chart")
                        st.altair_chart(pie,use_container_width=True)





        
        elif "Category" in st.session_state.modes:
            pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
            m=leafmap.Map(center=[40, -100], zoom=4)
            m.add_geojson(regions, layer_name="Countries",zoom_to_layer=False)



            if"Inscription Date" in st.session_state.modes:
                Cate_data=heritage[heritage['DATEINSCRI']==Inscdate]
                if Cate_data.empty:
                    m.add_basemap(basemap)
                    m.to_streamlit(height=700)
                    time_ct_group=pd.DataFrame({"Types":["Cultural","Mixed","Natural"],"CATSHORT":["C","C/N","N"],"count":[0,0,0]})
                else:
                    ct_group=to_df(Cate_data,"CATSHORT")
                    ct_group.rename(columns={0:'count'},inplace=True)
                    df_group=pd.DataFrame({"Types":["Cultural","Mixed","Natural"],"CATSHORT":["C","C/N","N"]})
                    time_ct_group=pd.merge(ct_group,df_group,how='outer', on="CATSHORT").fillna(0)
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
                pivot_tb=heritage.pivot_table(index='DATEINSCRI',
                                              columns='CATSHORT',
                                              values='CRITERIA',
                                              aggfunc='count',
                                              fill_value=0).round(decimals=2)
                col7,col8=st.columns([3,1])
                st.write("#### Pivot Table:")
                st.dataframe(data=pivot_tb,use_container_width=True)


                
                with col8:
                    chart_mode=['Line Chart','Bar Chart','Cumulative Line Chart']
                    Chart_mode=st.selectbox("Select a Mode",chart_mode)
                    years=to_df(heritage,'DATEINSCRI')
                    years['aggr']=0
                    years.rename(columns={0:'count'},inplace=True)
                    years=pd.merge(years,pivot_tb,on='DATEINSCRI',how='outer')
                    for i in range(Dateint,Dateend):
                        if i not in years['DATEINSCRI'].values:
                            Nu_data={'DATEINSCRI':[i],
                                     'count':[0],
                                     'aggr':[0],
                                     'C':[0],
                                     'C/N':[0],
                                     'N':[0]}
                            years=pd.concat([years,pd.DataFrame(Nu_data)],ignore_index=True)
                    st.write(years)   
                    pp=years[years['DATEINSCRI']==Inscdate]
                    d=pp['count'].to_list()[0]
                    st.write("Year:",Inscdate)
                    st.write("Total:",d)
                with col7:
                    cuml(years, 'count')
                    cond=alt.condition(alt.datum.Types==types,alt.value('red'),alt.value('steelblue'))
                    if types=="See All":
                        charts1=muti_chart(years,'N','green')+muti_chart(years,'C','orange')+muti_chart(years,'C/N','steelblue')
                    elif types=="Cultural":
                        charts1=muti_chart(years,'C','orange')
                    elif types=="Natural":
                        charts1=muti_chart(years,'N','green')
                    elif types=="Mixed":
                        charts1=muti_chart(years,'C/N','steelblue')
                    charts2 = alt.Chart(time_ct_group).mark_bar(size=10).encode(x=alt.X("Types",type='nominal'),y=alt.Y("count",type="quantitative"),color=cond)
                    charts3= alt.Chart(years).mark_line().encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("agrr",type="quantitative"))
                    if Chart_mode=='Line Chart':
                        st.altair_chart(charts1,use_container_width=True)
                    if Chart_mode=='Bar Chart':
                        st.altair_chart(charts2,use_container_width=True)
                    if Chart_mode=='Cumulative Line Chart':
                        st.altair_chart(charts3,use_container_width=True)


            
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
            m=leafmap.Map(center=[40, -100], zoom=4)
            Insc=heritage[heritage['DATEINSCRI']==Inscdate]
            m.add_geojson(regions, layer_name="Countries")
            m.add_points_from_xy(Insc,x="LONGITUDE",y="LATITUDE", popup=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE","CATFIN"])
            m.add_basemap(basemap)
            m.to_streamlit(height=700)
            col3,col4=st.columns([3,1])
            with col4:
                chart_mode=['Line Chart','Bar Chart','Cumulative Line Chart']
                Chart_mode=st.selectbox("Select a Mode",chart_mode)
                years=to_df(heritage,'DATEINSCRI')
                years['aggr']=0
                years.rename(columns={0:'count'},inplace=True)
                for i in range(Dateint,Dateend):
                    if i not in years['DATEINSCRI'].values:
                        Nu_data={'DATEINSCRI':[i],
                                 'count':[0],
                                 'aggr':[0]}
                        years=pd.concat([years,pd.DataFrame(Nu_data)],ignore_index=True)
                st.write(years)   
                pp=years[years['DATEINSCRI']==Inscdate]
                d=pp['count'].to_list()[0]
                st.write("Year:",Inscdate)
                st.write("Total:",d)
            with col3:
                cuml(years, 'count')
                cond=alt.condition(alt.datum.DATEINSCRI==Inscdate,alt.value('red'),alt.value('steelblue'))
                line_charts = alt.Chart(years).mark_line().encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("count",type="quantitative"))
                point_charts=alt.Chart(years).mark_point(filled=True,opacity=1).encode(x=alt.X("DATEINSCRI", type='temporal'),y=alt.Y("count", type="quantitative"),color=cond)
                charts1=line_charts+point_charts
                charts2 = alt.Chart(years).mark_bar(size=10).encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("count",type="quantitative"),color=cond)
                charts3= alt.Chart(years).mark_line().encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("aggr",type="quantitative"))
                if Chart_mode=='Line Chart':
                    st.altair_chart(charts1,use_container_width=True)
                if Chart_mode=='Bar Chart':
                    st.altair_chart(charts2,use_container_width=True)
                if Chart_mode=='Cumulative Line Chart':
                    st.altair_chart(charts3,use_container_width=True)
        else:
            st.write("Nothing Found")
    else:
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        
