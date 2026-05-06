from fastapi import FastAPI

app = FastAPI()

@app.get("/grade_calculator")
def grade_calculator(maths_score: int, physics_score: int, chemistry_score: int):
    total = maths_score + physics_score + chemistry_score
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
        "maths_score": maths_score,
        "physics_score": physics_score,
        "chemistry_score": chemistry_score,
        "total": total,
        "average": average,
        "grade": grade
    }
