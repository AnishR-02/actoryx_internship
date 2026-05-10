import gradio as gr

def factors(n):
    n = int(n)
    factors_list = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            factors_list.append(i)
    factors_list.append(n)
    return f"Factors of {n}: {factors_list}\nTotal factors: {len(factors_list)}"

app = gr.Interface(
    fn=factors,
    inputs=gr.Number(label="Enter a number", precision=0),
    outputs=gr.Text(label="Result"),
    title="Factors of a Number 🔍"
)

app.launch()
