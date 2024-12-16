import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

st.title("Feedback")
sug=st.text_input("Suggestion:",key="sug")
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars",key='star')
but=st.button("Send Feedback")
st.session_state
if but:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.write("Thank you~")

