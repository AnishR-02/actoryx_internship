from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    n: int

@app.post("/factors")
def factors(data: NumberInput):
    factors_list = []
    for i in range(1, data.n // 2 + 1):
        if data.n % i == 0:
            factors_list.append(i)
    factors_list.append(data.n)
    return {"number": data.n, "factors": factors_list, "total_factors": len(factors_list)}
