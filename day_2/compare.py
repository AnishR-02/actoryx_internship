from fastapi import FastAPI

app = FastAPI()

@app.get("/compare")
def compare(num1: int, num2: int):
    if num1 > num2:
        return {"result": f"{num1} is bigger"}
    elif num1 < num2:
        return {"result": f"{num2} is bigger"}
    else:
        return {"result": f"{num1} is equal to {num2}"}
