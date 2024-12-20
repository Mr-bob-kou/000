import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize page title
st.title("歡迎來到世界遺產導覽網站(現階段只有英文喔~~)")
st.header("網站資源")
st.write(
    """
    1. 世界遺產介紹(維基百科):[點我前往](https://zh.wikipedia.org/zh-tw/%E4%B8%96%E7%95%8C%E9%81%97%E4%BA%A7)
    2. 聯合國文教科組織世界遺產中心:[點我前往](https://whc.unesco.org/)
    """
)

st.header("介紹")

markdown = """
1. For the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template) or [use it as a template](https://github.com/giswqs/streamlit-multipage-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
