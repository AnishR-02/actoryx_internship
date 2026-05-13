import streamlit as st

st.title("Positive, Negative or Zero?")

num = st.number_input("Enter a number:", step=1, value=0)

if st.button("Check"):
    if num > 0:
        st.success(f"{num} is Positive ➕")
    elif num < 0:
        st.error(f"{num} is Negative ➖")
    else:
        st.info("The number is Zero 0️⃣")
