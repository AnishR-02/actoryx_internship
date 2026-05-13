import streamlit as st
import pandas as pd

st.title("CSV File Viewer 📊")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("First 10 Records:")
    st.dataframe(df.head(10))
