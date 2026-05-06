from fastapi import FastAPI

app = FastAPI()

@app.get("/sum_of_digits")
def sum_of_digits(n: int):
    original = n
    total = 0
    while n > 0:
        rem = n % 10
        total += rem
        n = n // 10
    return {"number": original, "sum_of_digits": total}
