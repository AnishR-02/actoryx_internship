import gradio as gr
import pandas as pd

def csv_viewer(file):
    df = pd.read_csv(file.name)
    return df.head(10)

app = gr.Interface(
    fn=csv_viewer,
    inputs=gr.File(label="Upload a CSV file"),
    outputs=gr.Dataframe(label="First 10 Records"),
    title="CSV File Viewer 📊"
)

app.launch()
