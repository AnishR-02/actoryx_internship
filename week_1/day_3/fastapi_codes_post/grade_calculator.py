from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GradeInput(BaseModel):
    maths_score: int
    physics_score: int
    chemistry_score: int

@app.post("/grade_calculator")
def grade_calculator(data: GradeInput):
    total = data.maths_score + data.physics_score + data.chemistry_score
    average = total // 3

    if average > 90:
        grade = "A+"
    elif average > 80:
        grade = "A"
    elif average > 70:
        grade = "B"
    elif average > 60:
        grade = "C"
    elif average > 50:
        grade = "D"
    else:
        grade = "F"

    return {
        "maths_score": data.maths_score,
        "physics_score": data.physics_score,
        "chemistry_score": data.chemistry_score,
        "total": total,
        "average": average,
        "grade": grade
    }
