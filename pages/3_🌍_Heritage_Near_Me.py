import streamlit as st
import leafmap.foliumap as leafmap

markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""
datum=st.session_state.heritage1
lon="LONGITUDE"
lat="LATITUDE"


st.title("Heritage Near Me")
col1,col2=st.columns([4,1])
col3, col4 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")
with col1:
    col5,col6,col7= st.columns([1,1,1])
    with col5:
        x_cord=st.text_input("Longitude")
    with col6:
        y_cord=st.text_input("Latitude")
    with col7:
        button=st.button("Searching")
with col4:

    basemap = st.selectbox("Select a basemap:", options, index)
    chx=st.toggle("Activate function A ?(Premium Member Only)")


with col3:

    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_points_from_xy(datum,x=lon,y=lat,popup=['NAME','COUNTRY','REGION','DATEINSCRI'])
    m.add_basemap(basemap)
    m.to_streamlit(height=700)
