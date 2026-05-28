import streamlit as st

st.title("Factors of a Number 🔍")

n = st.number_input("Enter a number:", step=1, min_value=1, value=1)

if st.button("Find Factors"):
    factors = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            factors.append(i)
    factors.append(n)

    st.success(f"Factors of {n} ✅")
    st.subheader("Here are the factors:")
    for factor in factors:
        st.write(factor)

    st.info(f"Total number of factors: {len(factors)}")
