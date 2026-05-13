from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/sum_of_list")
def sum_of_list(numbers: List[int] = Query(...)):
    total = sum(numbers)
    average = total / len(numbers)
    return {
        "numbers": numbers,
        "sum": total,
        "average": round(average, 2)
    }
