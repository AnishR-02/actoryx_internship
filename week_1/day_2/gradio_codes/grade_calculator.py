import gradio as gr

def grade_calculator(maths_score, physics_score, chemistry_score):
    total = maths_score + physics_score + chemistry_score
    average = total // 3

    if average > 90:
        grade = "A+"
    elif average > 80:
        grade = "A"
    elif average > 70:
        grade = "B"
    elif average > 60:
        grade = "C"
    elif average > 50:
        grade = "D"
    else:
        grade = "F"

    return f"Maths: {maths_score}\nPhysics: {physics_score}\nChemistry: {chemistry_score}\nTotal: {total}\nAverage: {average}\nGrade: {grade}"

app = gr.Interface(
    fn=grade_calculator,
    inputs=[
        gr.Number(label="Maths Score", precision=0),
        gr.Number(label="Physics Score", precision=0),
        gr.Number(label="Chemistry Score", precision=0)
    ],
    outputs=gr.Text(label="Result"),
    title="Grade Calculator 📝"
)

app.launch()
