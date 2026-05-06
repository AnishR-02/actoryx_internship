from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.get("/csv_viewer")
async def csv_viewer(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    first_10 = df.head(10).to_dict(orient="records")
    return {"first_10_records": first_10}
