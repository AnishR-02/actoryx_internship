import streamlit as st

st.title("Grade Calculator 📝")

maths_score = st.number_input("Enter Maths score:", step=1, min_value=0, max_value=100, value=0)
physics_score = st.number_input("Enter Physics score:", step=1, min_value=0, max_value=100, value=0)
chemistry_score = st.number_input("Enter Chemistry score:", step=1, min_value=0, max_value=100, value=0)

if st.button("Calculate Grade"):
    total = maths_score + physics_score + chemistry_score
    average = total // 3

    if average > 90:
        grade = "A+"
        st.success(f"Grade: {grade} 🌟")
    elif average > 80:
        grade = "A"
        st.success(f"Grade: {grade} 😊")
    elif average > 70:
        grade = "B"
        st.info(f"Grade: {grade} 👍")
    elif average > 60:
        grade = "C"
        st.info(f"Grade: {grade} 😐")
    elif average > 50:
        grade = "D"
        st.warning(f"Grade: {grade} 😕")
    else:
        grade = "F"
        st.error(f"Grade: {grade} ❌")

    st.subheader("Score Breakdown:")
    st.write(f"Maths: {maths_score}")
    st.write(f"Physics: {physics_score}")
    st.write(f"Chemistry: {chemistry_score}")
    st.write(f"Total: {total}")
    st.write(f"Average: {average}")
