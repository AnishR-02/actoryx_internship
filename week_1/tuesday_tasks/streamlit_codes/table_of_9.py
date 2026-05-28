import streamlit as st

st.title("Multiplication Table of 9 9️⃣")

if st.button("Show Table"):
    st.subheader("Multiplication Table of 9")
    for i in range(1, 11):
        st.write(f"9 x {i} = {9 * i}")
