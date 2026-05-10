from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CompareInput(BaseModel):
    num1: int
    num2: int

@app.post("/compare")
def compare(data: CompareInput):
    if data.num1 > data.num2:
        return {"result": f"{data.num1} is bigger"}
    elif data.num1 < data.num2:
        return {"result": f"{data.num2} is bigger"}
    else:
        return {"result": f"{data.num1} is equal to {data.num2}"}
