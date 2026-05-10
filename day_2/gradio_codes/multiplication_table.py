import gradio as gr

def multiplication_table(n):
    table = "\n".join(f"{n} x {i} = {n * i}" for i in range(1, 11))
    return table

app = gr.Interface(
    fn=multiplication_table,
    inputs=gr.Number(label="Enter a number", precision=0),
    outputs=gr.Text(label="Multiplication Table"),
    title="Multiplication Table ✖️"
)

app.launch()
