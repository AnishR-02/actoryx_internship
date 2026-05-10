import streamlit as st

st.title("Sum of Digits ➕")

n = st.number_input("Enter a number:", step=1, min_value=0, value=0)

if st.button("Calculate Sum"):
    original = n
    total = 0
    while n > 0:
        rem = n % 10
        total += rem
        n = n // 10
    st.success(f"Sum of digits of {original} = {total} ✅")
