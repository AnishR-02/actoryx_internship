from fastapi import FastAPI

app = FastAPI()

@app.get("/voting")
def voting(age: int):
    if age >= 18:
        return {"result": "You are eligible to vote"}
    else:
        return {"result": f"You are not eligible to vote. You need to be {18 - age} more year(s) older."}
