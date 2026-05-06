from fastapi import FastAPI

app = FastAPI()

@app.get("/factors")
def factors(n: int):
    factors_list = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            factors_list.append(i)
    factors_list.append(n)
    return {"number": n, "factors": factors_list, "total_factors": len(factors_list)}
