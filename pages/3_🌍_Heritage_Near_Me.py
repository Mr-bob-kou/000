import streamlit as st
import leafmap.foliumap as leafmap
import geopy.distance as distance
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from folium.features import GeoJsonPopup, GeoJsonTooltip
from folium.plugins import MarkerCluster

datum=st.session_state.heritage1
lon="LONGITUDE"
lat="LATITUDE"
options = list(leafmap.basemaps.keys())
option1=["OpenStreetMap","Cartodb Positron","Cartodb dark_matter"]
index = options.index("OpenTopoMap")
muti_options=["The Nearest","Top 5","Top 10","See All"]

def calculate_distance(row):
    city_coordinates = (row['LATITUDE'], row['LONGITUDE'])
    return distance.geodesic(city_coordinates, home_city_coordinates).km

tooltip2 = GeoJsonTooltip(
    fields=["NAME", "COUNTRY", "DATEINSCRI"],
    aliases=["name:", "country:", "Inscribed Time"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

if 'cordx' not in st.session_state:
    st.session_state.cordx=""
if 'cordy' not in st.session_state:
    st.session_state.cordy=""
if 'chx' not in st.session_state:
    st.session_state.chx=False


st.title("Heritage Near Me")
st.session_state
col1,col2=st.columns([4,1])
col3, col4 = st.columns([4, 1])

with col1:
    col5,col6,col7= st.columns([2,2,1],vertical_alignment="bottom")
    with col5:
        x_cord=st.text_input("Longitude",value=st.session_state.cordx)
    with col6:
        y_cord=st.text_input("Latitude",value=st.session_state.cordy)
    with col7:
        button=st.button("Searching",key='search')
with col4:
    if st.session_state.chx==True:
        basemap_fol=st.selectbox("Select a basemap:", option1)
    else:
        basemap = st.selectbox("Select a basemap:", options, index)
    chx=st.toggle("Activate function A ?(Premium Member Only)",key="chx")
    
with col3:
    if chx:
        m1 = folium.Map(location=[0,0], zoom_start=1,tile=basemap_fol)
        Draw(export=True).add_to(m1)
        marker_cluster = MarkerCluster().add_to(m1)
        folium.GeoJson(
            datum.to_json(),
            name="Heritage",
            marker=folium.Marker(icon=folium.Icon(icon='info-sign')),
            tooltip=tooltip2).add_to(marker_cluster)
        output=st_folium(m1, use_container_width=True)
        if output["last_clicked"] is None:
            st.write("Click the map and get latitude and longitude!!")
        else:
            fol_lat=output["last_clicked"]['lat']
            fol_long=output["last_clicked"]['lng']
            if fol_long != st.session_state.cordx:
                st.session_state.cordx=fol_long
                st.rerun()
            if fol_lat!= st.session_state.cordy:
                st.session_state.cordy=fol_lat
                st.rerun()

        if st.session_state.search==True:
            home_city_coordinates =[y_cord,x_cord]
            result= datum.apply(calculate_distance, axis=1)
            datum['distance_from_home'] = result
            miun=datum[datum['distance_from_home']==datum['distance_from_home'].min()]
            name=miun["NAME"].to_string(index=False)
            mini_dis=miun["distance_from_home"].to_string(index=False)
            mult=st.segmented_control(" ",muti_options,default='The Nearest')
            if mult=="The Nearest":
                st.write("The Nearest Heritage is:",name )
                st.write("The Minimum Distance is:",mini_dis,"km" )
            elif mult=="Top 5":
                st.dataframe(data=datum.head(5))
            elif mult=="Top 10":
                st.dataframe(data=datum.head(10))
            elif mult=="See All":
                st.dataframe(data=datum)
            button2=st.button("Rerun")
            if button2:
                st.rerun()
    else:
        m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
        m.add_points_from_xy(datum,x=lon,y=lat,popup=['NAME','COUNTRY','REGION','DATEINSCRI'])
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        if st.session_state.search==True:
            home_city_coordinates =[y_cord,x_cord]
            result= datum.apply(calculate_distance, axis=1)
            datum['distance_from_home'] = result
            miun=datum[datum['distance_from_home']==datum['distance_from_home'].min()]
            name=miun["NAME"].to_string(index=False)
            mini_dis=miun["distance_from_home"].to_string(index=False)
            st.write("The Nearest Heritage is:",name )
            st.write("The Minimum Distance is:",mini_dis,"km" )
            button2=st.button("Rerun")
            if button2:
                st.rerun()
