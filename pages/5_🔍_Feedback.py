import streamlit as st
import leafmap.foliumap as leafmap
import time 

st.set_page_config(layout="wide")

st.title("Feedback")
sug=st.text_input("Suggestion:",key="sug")
sentiment_mapping = ["zero","one", "two", "three", "four", "five"]
selected = st.feedback("stars",key='star')
but=st.button("Send Feedback")
if but:
    st.write("Your Suggestion:",sug)
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
    st.write("Thank you~")
    st.balloons()
    time.sleep(3)
    st.rerun()

