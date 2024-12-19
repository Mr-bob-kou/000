import streamlit as st
import leafmap.foliumap as leafmap

markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""



st.title("Heritage Near Me")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:

    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_basemap(basemap)
    m.to_streamlit(height=700)
