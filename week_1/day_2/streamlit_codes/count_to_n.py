import streamlit as st

st.title("Count from 1 to N 🔄")

n = st.number_input("Enter a number:", step=1, min_value=1, value=1)

if st.button("Start Counting"):
    i = 1
    while i <= n:
        st.write(i)
        i += 1
    st.success(f"Done! Counted from 1 to {n} ✅")
