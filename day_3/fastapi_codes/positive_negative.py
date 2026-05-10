from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    num: int

@app.post("/positive_negative")
def positive_negative(data: NumberInput):
    if data.num > 0:
        return {"result": f"{data.num} is Positive"}
    elif data.num < 0:
        return {"result": f"{data.num} is Negative"}
    else:
        return {"result": "The number is Zero"}
