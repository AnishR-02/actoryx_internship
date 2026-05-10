import gradio as gr

def compare(num1, num2):
    if num1 > num2:
        return f"{num1} is bigger! 🏆"
    elif num1 < num2:
        return f"{num2} is bigger! 🏆"
    else:
        return f"{num1} is equal to {num2} 🟰"

app = gr.Interface(
    fn=compare,
    inputs=[
        gr.Number(label="Enter first number"),
        gr.Number(label="Enter second number")
    ],
    outputs=gr.Text(label="Result"),
    title="Compare Two Numbers"
)

app.launch()
