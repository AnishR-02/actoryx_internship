import streamlit as st

st.title("Simple Calculator 🧮")

num1 = st.number_input("Enter first number:", value=0.0)
num2 = st.number_input("Enter second number:", value=0.0)

operator = st.selectbox("Select an operator:", ["+", "-", "*", "/"])

if st.button("Calculate"):
    if operator == "+":
        st.success(f"{num1} + {num2} = {num1 + num2}")
    elif operator == "-":
        st.success(f"{num1} - {num2} = {num1 - num2}")
    elif operator == "*":
        st.success(f"{num1} * {num2} = {num1 * num2}")
    elif operator == "/":
        if num2 == 0:
            st.error("Error: Division by zero! ❌")
        else:
            st.success(f"{num1} / {num2} = {num1 / num2}")
