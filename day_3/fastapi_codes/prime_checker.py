from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NumberInput(BaseModel):
    n: int

@app.post("/prime_checker")
def prime_checker(data: NumberInput):
    if data.n < 2:
        return {"number": data.n, "result": f"{data.n} is not a prime number"}
    is_prime = True
    for i in range(2, data.n // 2 + 1):
        if data.n % i == 0:
            is_prime = False
            break
    if is_prime:
        return {"number": data.n, "result": f"{data.n} is a prime number"}
    else:
        return {"number": data.n, "result": f"{data.n} is not a prime number"}
