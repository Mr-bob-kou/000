import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import altair as alt
import pydeck as pdk
import math

st.set_page_config(layout="wide",page_title="My World Herritage Website", page_icon="☘️")
st.title("Main")
st.write("Test")
st.session_state
data="https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/main/point.geojson"
if 'heritage1' not in st.session_state:
    st.session_state.heritage1 = gpd.read_file(data)
heritage=st.session_state.heritage1
regions = "https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/main/world-administrative-boundaries.geojson"
data2="https://github.com/Mr-bob-kou/My_Respository/raw/main/World%20Heritage%20Counts.geojson"
Count=gpd.read_file(data2)
data3="https://raw.githubusercontent.com/Mr-bob-kou/My_Respository/refs/heads/main/point2.geojson"
heritage2=gpd.read_file(data3)
count10=Count.sort_values(by='count', ascending=False).head(10)
heritage_sort=heritage.sort_values(by='NAME', ascending=True)

options = list(leafmap.basemaps.keys())
index = options.index("OpenStreetMap")
modes=["Default","Heat Map","Choropleth Map(Heritage Count)","Inscribed Date","Catagory"]
modes1="Default"
opt=["See All"]+list(heritage_sort['NAME'])

legend_dict = {
    "0":'#FFFFFF',
    "0-10":'#D2E9FF',
    "10-20":'#ACD6FF',
    "20-30": '#46A3FF',
    "30-40": '#0066CC',
    "40+": '#003060',
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
def chromap(datum,mp):
    mp.add_basemap(basemap)
    mp.add_geojson(datum,style_callback=style_function) 
    mp.add_legend(title="Heritage Counts", legend_dict=legend_dict,draggable=False,position="bottomright")
    return mp.to_streamlit(height=700)
def heatmap(datum,mp,lat,lon,val):
    mp.add_heatmap(
        datum,
        latitude=lat,
        longitude=lon,
        value=val,
        name="Heat map",
        radius=20)
    return mp.to_streamlit(height=700)
def Default(datum,mp,lon,lat,pop):
    mp.add_geojson(regions, layer_name="Countries",zoom_to_layer=False)
    mp.add_points_from_xy(datum,x=lon,y=lat, popup=pop)
    mp.add_basemap(basemap)
    return mp.to_streamlit(height=700)

def to_df(datum,val):
    couda=datum.groupby(val).size()
    couda.to_frame()
    return couda.reset_index()
def cuml(datum,val):
    datum['aggr']=0
    for i in datum.index:
        if i==0:
            datum['aggr'][i]=datum[val][i]
        else:
            datum['aggr'][i]=datum[val][i]+datum['aggr'][i-1]
    return datum
def Info(NAME,COUNTRY,DESC):
    st.write("INFO:")
    st.write("Heritage Name:",NAME)
    st.write("Country:",COUNTRY)
    st.write("Description:",DESC)

def color_scale(val):
    for i, b in enumerate(BREAKS):
        if val <= b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]
def calculate_elevation(val):
    return math.sqrt(val) * 20000

Count["elevation"] = Count['count'].apply(calculate_elevation)
Count["filled_color"]=Count['count'].apply(color_scale)

with st.expander("See All Heritage Data"):
    st.dataframe(data=heritage, use_container_width=True)
col1, col2 = st.columns([4, 1])

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)
    mode=st.selectbox("Select a Mode",modes)
    if mode=='Choropleth Map(Heritage Count)':
        chbox=st.checkbox("3-D Presentation")
    if mode=="Inscribed Date":
        Dateint=heritage['DATEINSCRI'].min()
        Dateend=heritage['DATEINSCRI'].max()
        Inscdate=st.slider("Choose the Year",Dateint,Dateend)
        st.write(Inscdate)
    if mode=="Default":
        place=st.selectbox("Choose a Place",opt)
        s=heritage[heritage['NAME']==place]
        if place=="See All":
            Info("NA","NA","NA")
        else:
            s=heritage[heritage['NAME']==place]
            h_name=s['NAME'].to_string(index=False)
            h_country=s['COUNTRY'].to_string(index=False)
            h_des=s['DESCRIPTIO'].to_string(index=False)
            Info(h_name,h_country,h_des)
with col1:
    m = leafmap.Map(center=[40, -100], zoom=4)
    if mode=='Choropleth Map(Heritage Count)':
        if chbox:
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
                    Count,
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
            st.write(deck)
        else:
           chromap(data2,m) 
        col3,col4=st.columns([2,2])
        with col3:
            st.write("#### Heritage Count Statistics(Top 10)")
            charts = alt.Chart(count10).mark_bar(size=20).encode(x=alt.X("name",type="nominal").sort("y"),y=alt.Y("count",type="quantitative"))
            st.altair_chart(charts,use_container_width=True)
        with col4:
            st.write("#### Heritage Count Pie Chart")
            pie=alt.Chart(Count).mark_arc().encode(theta="count",color="name")
            st.altair_chart(pie,use_container_width=True)
            
    elif mode=='Heat Map':
       heatmap(heritage2,m,"LATITUDE","LONGITUDE","AREAHA")
        
    elif mode=='Default':
        if place=='See All':
            m1 = leafmap.Map(center=[0,0], zoom=1,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
            pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
            Default(heritage,m1, "LONGITUDE","LATITUDE",pop)
        else:
            lat=s['LATITUDE'].to_string(index=False)
            long=s['LONGITUDE'].to_string(index=False)
            centers=[lat,long]
            m7 = leafmap.Map(center=centers,zoom=15,locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
            pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
            Default(heritage,m7, "LONGITUDE","LATITUDE",pop)

    elif mode=="Catagory":
        pop=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"]
        m=leafmap.Map(center=[40, -100], zoom=4)
        m.add_geojson(regions, layer_name="Countries",zoom_to_layer=False)
        m.add_points_from_xy(heritage,x="LONGITUDE",y="LATITUDE", popup=pop,color_column='CATSHORT',marker_colors=['white','green','red'],icon_colors=['white','green','red'])
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        
    elif mode=="Inscribed Date":
        m=leafmap.Map(center=[40, -100], zoom=4)
        Insc=heritage[heritage['DATEINSCRI']==Inscdate]
        m.add_geojson(regions, layer_name="Countries")
        m.add_points_from_xy(Insc,x="LONGITUDE",y="LATITUDE", popup=["NAME","DATEINSCRI","COUNTRY","DESCRIPTIO","AREAHA","DANGER","LONGITUDE","LATITUDE"])
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        col3,col4=st.columns([3,1])
        with col4:
            chart_mode=['Line Chart','Bar Chart','Cumulative Line Chart']
            Chart_mode=st.selectbox("Select a Mode",chart_mode)
            years=to_df(heritage,'DATEINSCRI')
            years['aggr']=0
            years.rename(columns={0:'count'},inplace=True)
            pp=years[years['DATEINSCRI']==Inscdate]
            d=pp['count'].to_list()[0]
            st.write("Year:",Inscdate)
            st.write("Total:",d)
        with col3:
            cuml(years, 'count')
            cond=alt.condition(alt.datum.DATEINSCRI==Inscdate,alt.value('red'),alt.value('steelblue'))
            charts1 = alt.Chart(years).mark_line(point=True).encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("count",type="quantitative"),color=cond)
            charts2 = alt.Chart(years).mark_bar(size=10).encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("count",type="quantitative"),color=cond)
            charts3= alt.Chart(years).mark_line().encode(x=alt.X("DATEINSCRI",type='temporal'),y=alt.Y("aggr",type="quantitative"))
            if Chart_mode=='Line Chart':
                st.altair_chart(charts1,use_container_width=True)
            if Chart_mode=='Bar Chart':
                st.altair_chart(charts2,use_container_width=True)
            if Chart_mode=='Cumulative Line Chart':
                st.altair_chart(charts3,use_container_width=True)
