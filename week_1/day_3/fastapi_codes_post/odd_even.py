from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    num: int

@app.post("/odd_even")
def odd_even(data: NumberInput):
    if data.num % 2 == 0:
        return {"result": "The number is Even"}
    else:
        return {"result": "The number is Odd"}
