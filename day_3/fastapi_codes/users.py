from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# In-memory database (just for demo)
users = {}

# Pydantic Model
class User(BaseModel):
    name: str
    age: int


# ----------------------
# GET - Root
# ----------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}


# ----------------------
# GET - Get All Users
# ----------------------
@app.get("/users")
async def get_users():
    return users


# ----------------------
# GET - Get One User
# ----------------------
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


# ----------------------
# POST - Create User
# ----------------------
@app.post("/users/{user_id}")
async def create_user(user_id: int, user: User):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user_id] = user.dict()
    return {"message": "User created successfully", "user": users[user_id]}


# ----------------------
# PUT - Update User
# ----------------------
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = user.dict()
    return {"message": "User updated successfully", "user": users[user_id]}


# ----------------------
# DELETE - Delete User
# ----------------------
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": "User deleted successfully"}


# ----------------------
# Auto Start
# ----------------------
if __name__ == "__main__":
    uvicorn.run("Users:app", host="127.0.0.1", port=8012, reload=True)