import streamlit as st

st.title("Prime Number Checker 🔢")

n = st.number_input("Enter a number:", step=1, min_value=0, value=0)

if st.button("Check"):
    if n < 2:
        st.error(f"{n} is not a prime number ❌")
    else:
        is_prime = True
        for i in range(2, n // 2 + 1):
            if n % i == 0:
                is_prime = False
                break

        if is_prime:
            st.success(f"{n} is a Prime number ✅")
            st.info(f"{n} is only divisible by 1 and {n}")
        else:
            st.error(f"{n} is not a Prime number ❌")
            st.info(f"It is divisible by {[i for i in range(2, n) if n % i == 0]}")
