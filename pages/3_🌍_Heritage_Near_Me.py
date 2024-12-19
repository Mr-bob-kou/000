import streamlit as st
import leafmap.foliumap as leafmap
import geopy.distance


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
with col1:
    col5,col6,col7= st.columns([2,2,1],vertical_alignment="bottom")
    with col5:
        x_cord=st.text_input("Longitude")
    with col6:
        y_cord=st.text_input("Latitude")
    with col7:
        button=st.button("Searching",key='search')
with col4:

    basemap = st.selectbox("Select a basemap:", options, index)
    chx=st.toggle("Activate function A ?(Premium Member Only)")


with col3:
    if st.session_state.search==True:
        home_city_coordinates =[x_cord,y_cord]
        result= datum.apply(calculate_distance, axis=1)
        datum['distance_from_home'] = result
        miun=datum[datum['distance_from_home']==datum['distance_from_home'].min()]
        name=miun["NAME"]
        st.write("The Nearest Heritage is:",name )
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_points_from_xy(datum,x=lon,y=lat,popup=['NAME','COUNTRY','REGION','DATEINSCRI'])
    m.add_basemap(basemap)
    m.to_streamlit(height=700)
