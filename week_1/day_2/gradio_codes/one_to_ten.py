import gradio as gr

def one_to_ten():
    return "\n".join(str(i) for i in range(1, 11))

app = gr.Interface(
    fn=one_to_ten,
    inputs=[],
    outputs=gr.Text(label="Numbers"),
    title="Numbers 1 to 10 🔢"
)

app.launch()
