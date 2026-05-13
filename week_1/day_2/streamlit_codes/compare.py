import streamlit as st

st.title("Compare Two Numbers")

num1 = st.number_input("Enter the first number:", step=1, value=0)
num2 = st.number_input("Enter the second number:", step=1, value=0)

if st.button("Compare"):
    if num1 > num2:
        st.success(f"{num1} is bigger! 🏆")
    elif num1 < num2:
        st.success(f"{num2} is bigger! 🏆")
    else:
        st.info(f"{num1} is equal to {num2} 🟰")
