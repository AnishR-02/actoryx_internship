from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AgeInput(BaseModel):
    age: int

@app.post("/voting")
def voting(data: AgeInput):
    if data.age >= 18:
        return {"result": "You are eligible to vote"}
    else:
        return {"result": f"You are not eligible to vote. You need to be {18 - data.age} more year(s) older."}
