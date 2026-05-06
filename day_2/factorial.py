from fastapi import FastAPI

app = FastAPI()

@app.get("/factorial")
def factorial(n: int):
    if n < 0:
        return {"result": "Factorial is not defined for negative numbers"}
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i
    return {"number": n, "factorial": fact}
