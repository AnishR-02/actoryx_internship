import gradio as gr

def calculator(num1, operator, num2):
    if operator == "+":
        return f"{num1} + {num2} = {num1 + num2}"
    elif operator == "-":
        return f"{num1} - {num2} = {num1 - num2}"
    elif operator == "*":
        return f"{num1} * {num2} = {num1 * num2}"
    elif operator == "/":
        if num2 == 0:
            return "Error: Division by zero! ❌"
        else:
            return f"{num1} / {num2} = {num1 / num2}"
    else:
        return "Invalid operator!"

app = gr.Interface(
    fn=calculator,
    inputs=[
        gr.Number(label="Enter first number"),
        gr.Dropdown(choices=["+", "-", "*", "/"], label="Select operator"),
        gr.Number(label="Enter second number")
    ],
    outputs=gr.Text(label="Result"),
    title="Simple Calculator 🧮"
)

app.launch()
