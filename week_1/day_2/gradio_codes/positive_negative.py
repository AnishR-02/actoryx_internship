import gradio as gr

def positive_negative(num):
    if num > 0:
        return f"{num} is Positive ➕"
    elif num < 0:
        return f"{num} is Negative ➖"
    else:
        return "The number is Zero 0️⃣"

app = gr.Interface(
    fn=positive_negative,
    inputs=gr.Number(label="Enter a number"),
    outputs=gr.Text(label="Result"),
    title="Positive, Negative or Zero?"
)

app.launch()
