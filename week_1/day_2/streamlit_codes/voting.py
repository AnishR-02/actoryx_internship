import streamlit as st

st.title("Voting Eligibility Checker")

age = st.number_input("Enter your age:", step=1, min_value=0, value=0)

if st.button("Check Eligibility"):
    if age >= 18:
        st.success("You are eligible to vote! ✅")
    else:
        st.error(f"You are not eligible to vote. You need to be {18 - age} more year(s) older. ❌")
