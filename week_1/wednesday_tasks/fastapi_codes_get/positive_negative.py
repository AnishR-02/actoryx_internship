from fastapi import FastAPI

app = FastAPI()

@app.get("/positive_negative")
def positive_negative(num: int):
    if num > 0:
        return {"result": f"{num} is Positive"}
    elif num < 0:
        return {"result": f"{num} is Negative"}
    else:
        return {"result": "The number is Zero"}
