import gradio as gr

def odd_even(num):
    if num % 2 == 0:
        return "The number is Even ✅"
    else:
        return "The number is Odd 🔢"

app = gr.Interface(
    fn=odd_even,
    inputs=gr.Number(label="Enter a number"),
    outputs=gr.Text(label="Result"),
    title="Odd or Even Checker"
)

app.launch()
