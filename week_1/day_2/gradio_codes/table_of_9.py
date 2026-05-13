import gradio as gr

def table_of_9():
    table = "\n".join(f"9 x {i} = {9 * i}" for i in range(1, 11))
    return table

app = gr.Interface(
    fn=table_of_9,
    inputs=[],
    outputs=gr.Text(label="Multiplication Table of 9"),
    title="Multiplication Table of 9 9️⃣"
)

app.launch()
