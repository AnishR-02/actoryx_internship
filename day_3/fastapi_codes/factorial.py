from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    n: int

@app.post("/factorial")
def factorial(data: NumberInput):
    if data.n < 0:
        return {"result": "Factorial is not defined for negative numbers"}
    fact = 1
    for i in range(1, data.n + 1):
        fact = fact * i
    return {"number": data.n, "factorial": fact}
