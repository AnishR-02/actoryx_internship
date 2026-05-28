from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/csv_viewer")
def csv_viewer(file_path: str):
    df = pd.read_csv(file_path)
    first_10 = df.head(10).to_dict(orient="records")
    return {"first_10_records": first_10}
