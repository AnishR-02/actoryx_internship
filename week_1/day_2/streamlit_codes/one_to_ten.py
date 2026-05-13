import streamlit as st

st.title("Numbers 1 to 10 🔢")

if st.button("Show Numbers"):
    for i in range(1, 11):
        st.write(i)
