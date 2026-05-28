from fastapi import FastAPI

app = FastAPI()

@app.get("/prime_checker")
def prime_checker(n: int):
    if n < 2:
        return {"number": n, "result": f"{n} is not a prime number"}
    is_prime = True
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            is_prime = False
            break
    if is_prime:
        return {"number": n, "result": f"{n} is a prime number"}
    else:
        return {"number": n, "result": f"{n} is not a prime number"}
