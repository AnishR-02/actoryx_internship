import gradio as gr

def sum_of_digits(n):
    n = int(n)
    original = n
    total = 0
    while n > 0:
        rem = n % 10
        total += rem
        n = n // 10
    return f"Sum of digits of {original} = {total} ✅"

app = gr.Interface(
    fn=sum_of_digits,
    inputs=gr.Number(label="Enter a number", precision=0),
    outputs=gr.Text(label="Result"),
    title="Sum of Digits ➕"
)

app.launch()
