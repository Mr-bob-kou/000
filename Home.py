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

st.header("功能介紹")

markdown = """
1. 主要平台:對於世界遺產進行介紹(Default)以及其分析統計.
2. 最近的世界遺產:查詢最近於使用者的世界遺產(目前沒有定位功能)
3. 增加世界遺產:使用者可以自行增加世界遺產喔!

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
