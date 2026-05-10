from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    n: int

@app.post("/count_to_n")
def count_to_n(data: NumberInput):
    numbers = []
    i = 1
    while i <= data.n:
        numbers.append(i)
        i += 1
    return {"numbers": numbers}
