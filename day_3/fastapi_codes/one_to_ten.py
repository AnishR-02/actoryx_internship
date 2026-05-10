from fastapi import FastAPI

app = FastAPI()

@app.post("/one_to_ten")
def one_to_ten():
    numbers = [i for i in range(1, 11)]
    return {"numbers": numbers}
