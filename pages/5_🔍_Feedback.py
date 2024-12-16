import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

st.title("Feedback")
sug=st.text_input("Suggestion:")
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
but=st.button("Send Feedback")
if but:
    @st.dialog("Thank You~", width="small")
    st.write("Thanks~~~")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

