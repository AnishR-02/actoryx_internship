from fastapi import FastAPI

app = FastAPI()

@app.get("/odd_even")
def odd_even(num: int):
    if num % 2 == 0:
        return {"result": "The number is Even"}
    else:
        return {"result": "The number is Odd"}
