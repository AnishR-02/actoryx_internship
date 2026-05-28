from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    n: int

@app.post("/sum_of_digits")
def sum_of_digits(data: NumberInput):
    original = data.n
    n = data.n
    total = 0
    while n > 0:
        rem = n % 10
        total += rem
        n = n // 10
    return {"number": original, "sum_of_digits": total}
