import streamlit as st

st.title("Sum of a List of Numbers ➕")

n = st.number_input("How many numbers do you want to add?", step=1, min_value=1, value=1)

numbers = []
for i in range(n):
    num = st.number_input(f"Enter number {i + 1}:", step=1, value=0, key=f"num_{i}")
    numbers.append(num)

if st.button("Calculate Sum"):
    total = 0
    for i in range(n):
        total += numbers[i]

    st.success(f"Your numbers: {numbers}")
    st.success(f"Sum = {total} ✅")
    st.info(f"Average = {total / n:.2f}")
