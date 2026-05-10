from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    n: int

@app.post("/multiplication_table")
def multiplication_table(data: NumberInput):
    table = {f"{data.n} x {i}": data.n * i for i in range(1, 11)}
    return {"multiplication_table": table}
