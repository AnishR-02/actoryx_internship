import streamlit as st

st.title("Factorial Calculator ❗")

n = st.number_input("Enter a number:", step=1, min_value=0, value=0)

if st.button("Calculate Factorial"):
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i
    st.success(f"Factorial of {n} = {fact} ✅")

    st.subheader("How it was calculated:")
    steps = " x ".join(str(i) for i in range(1, n + 1))
    if n == 0:
        st.write("0! = 1 (by definition)")
    else:
        st.write(f"{n}! = {steps} = {fact}")
