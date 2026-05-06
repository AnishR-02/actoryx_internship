from fastapi import FastAPI

app = FastAPI()

@app.get("/calculator")
def calculator(num1: float, operator: str, num2: float):
    if operator == "+":
        return {"result": f"{num1} + {num2} = {num1 + num2}"}
    elif operator == "-":
        return {"result": f"{num1} - {num2} = {num1 - num2}"}
    elif operator == "*":
        return {"result": f"{num1} * {num2} = {num1 * num2}"}
    elif operator == "/":
        if num2 == 0:
            return {"result": "Error: Division by zero!"}
        else:
            return {"result": f"{num1} / {num2} = {num1 / num2}"}
    else:
        return {"result": "Invalid operator! Use +, -, *, /"}
