from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CalculatorInput(BaseModel):
    num1: float
    operator: str
    num2: float

@app.post("/calculator")
def calculator(data: CalculatorInput):
    if data.operator == "+":
        return {"result": f"{data.num1} + {data.num2} = {data.num1 + data.num2}"}
    elif data.operator == "-":
        return {"result": f"{data.num1} - {data.num2} = {data.num1 - data.num2}"}
    elif data.operator == "*":
        return {"result": f"{data.num1} * {data.num2} = {data.num1 * data.num2}"}
    elif data.operator == "/":
        if data.num2 == 0:
            return {"result": "Error: Division by zero!"}
        else:
            return {"result": f"{data.num1} / {data.num2} = {data.num1 / data.num2}"}
    else:
        return {"result": "Invalid operator! Use +, -, *, /"}
