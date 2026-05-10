from fastapi import FastAPI

app = FastAPI()

@app.post("/table_of_9")
def table_of_9():
    table = {f"9 x {i}": 9 * i for i in range(1, 11)}
    return {"multiplication_table_of_9": table}
