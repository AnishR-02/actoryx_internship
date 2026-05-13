import streamlit as st

st.title("Multiplication Table ✖️")

n = st.number_input("Enter a number:", step=1, value=1)

if st.button("Show Table"):
    st.subheader(f"Multiplication Table of {n}")
    for i in range(1, 11):
        st.write(f"{n} x {i} = {n * i}")
