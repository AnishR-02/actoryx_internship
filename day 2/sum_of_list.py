from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/sum_of_list")
def sum_of_list(numbers: str):
    number_list = [int(x) for x in numbers.split(",")]
    total = sum(number_list)
    average = total / len(number_list)
    return {
        "numbers": number_list,
        "sum": total,
        "average": round(average, 2)
    }
