from fastapi import FastAPI

app = FastAPI()

@app.get("/count_to_n")
def count_to_n(n: int):
    numbers = []
    i = 1
    while i <= n:
        numbers.append(i)
        i += 1
    return {"numbers": numbers}
