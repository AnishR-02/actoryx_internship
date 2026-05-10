import gradio as gr

def voting(age):
    if age >= 18:
        return "You are eligible to vote! ✅"
    else:
        return f"You are not eligible to vote. You need to be {18 - age} more year(s) older. ❌"

app = gr.Interface(
    fn=voting,
    inputs=gr.Number(label="Enter your age"),
    outputs=gr.Text(label="Result"),
    title="Voting Eligibility Checker"
)

app.launch()
