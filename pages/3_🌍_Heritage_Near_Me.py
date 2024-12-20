import streamlit as st
import leafmap.foliumap as leafmap
import geopy.distance as distance
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw


datum=st.session_state.heritage1
lon="LONGITUDE"
lat="LATITUDE"
def calculate_distance(row):
    city_coordinates = (row['LATITUDE'], row['LONGITUDE'])
    return distance.geodesic(city_coordinates, home_city_coordinates).km

st.title("Heritage Near Me")
col1,col2=st.columns([4,1])
col3, col4 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")
st.session_state
with col1:
    col5,col6,col7= st.columns([2,2,1],vertical_alignment="bottom")
    with col5:
        x_cord=st.text_input("Longitude",key='cordx')
    with col6:
        y_cord=st.text_input("Latitude",key='cordy')
    with col7:
        button=st.button("Searching",key='search')
with col4:

    basemap = st.selectbox("Select a basemap:", options, index)
    chx=st.toggle("Activate function A ?(Premium Member Only)",)


with col3:
    if chx:
        st.write("waiter")
        m1 = folium.Map(location=[39.949610, -75.150282], zoom_start=5,tile=basemap)
        Draw(export=True).add_to(m1)
        output=st_folium(m1, width=700, height=500)
        fol_lat=output["last_clicked"]['lat']
        fol_long=output["last_clicked"]['lng']
        st.write(127)
        #st.session_state.cordx=float(fol_long)
        #st.session_state.cordy=float(fol_lat)
    else:
        m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
        m.add_points_from_xy(datum,x=lon,y=lat,popup=['NAME','COUNTRY','REGION','DATEINSCRI'])
        m.add_basemap(basemap)
        m.to_streamlit(height=700)
        st.write(m)
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
