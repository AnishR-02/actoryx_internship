from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class NumbersInput(BaseModel):
    numbers: List[int]

@app.post("/sum_of_list")
def sum_of_list(data: NumbersInput):
    total = sum(data.numbers)
    average = total / len(data.numbers)
    return {
        "numbers": data.numbers,
        "sum": total,
        "average": round(average, 2)
    }
