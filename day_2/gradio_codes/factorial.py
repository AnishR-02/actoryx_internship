import gradio as gr

def factorial(n):
    n = int(n)
    if n < 0:
        return "Factorial is not defined for negative numbers"
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i
    if n == 0:
        steps = "0! = 1 (by definition)"
    else:
        steps = " x ".join(str(i) for i in range(1, n + 1))
        steps = f"{n}! = {steps} = {fact}"
    return f"Factorial of {n} = {fact} ✅\n\n{steps}"

app = gr.Interface(
    fn=factorial,
    inputs=gr.Number(label="Enter a number", precision=0),
    outputs=gr.Text(label="Result"),
    title="Factorial Calculator ❗"
)

app.launch()
