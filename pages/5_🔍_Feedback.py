import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

st.title("Feedback")
sug=st.text_input("Suggestion:")
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
but=st.button("Send Feedback")
if but:
    st.write("Thank you~")

