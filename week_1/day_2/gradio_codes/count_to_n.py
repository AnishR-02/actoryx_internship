import gradio as gr

def count_to_n(n):
    numbers = []
    i = 1
    while i <= n:
        numbers.append(str(i))
        i += 1
    return "\n".join(numbers)

app = gr.Interface(
    fn=count_to_n,
    inputs=gr.Number(label="Enter a number", precision=0),
    outputs=gr.Text(label="Count"),
    title="Count from 1 to N 🔄"
)

app.launch()
