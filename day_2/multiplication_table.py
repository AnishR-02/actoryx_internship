from fastapi import FastAPI

app = FastAPI()

@app.get("/multiplication_table")
def multiplication_table(n: int):
    table = {f"{n} x {i}": n * i for i in range(1, 11)}
    return {"multiplication_table": table}
