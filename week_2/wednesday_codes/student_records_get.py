from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="Student Records API",
    description="API to manage student academic records",
    version="1.0.0"
)

# --------------------------------------------------------------------------- #
# Data Models
# --------------------------------------------------------------------------- #

class Course(BaseModel):
    course_name: str = Field(..., example="Data Structures")
    course_code: str = Field(..., example="CS301")
    faculty: str = Field(..., example="Dr. Ramesh Kumar")


class StudentRecord(BaseModel):
    roll_no: str = Field(..., example="2024CS001")
    full_name: str = Field(..., example="Aanya Sharma")
    college_name: str = Field(..., example="Jawaharlal Nehru Engineering College")
    courses: List[Course] = Field(..., min_items=1)


# --------------------------------------------------------------------------- #
# In-memory "database"
# --------------------------------------------------------------------------- #

STUDENTS: dict[str, StudentRecord] = {
    "2024CS001": StudentRecord(
        roll_no="2024CS001",
        full_name="Aanya Sharma",
        college_name="Jawaharlal Nehru Engineering College",
        courses=[
            Course(course_name="Data Structures", course_code="CS301", faculty="Dr. Ramesh Kumar"),
            Course(course_name="Database Management", course_code="CS302", faculty="Prof. Sunita Rao"),
            Course(course_name="Operating Systems", course_code="CS303", faculty="Dr. Vikram Nair"),
        ],
    ),
    "2024ME042": StudentRecord(
        roll_no="2024ME042",
        full_name="Rohan Patel",
        college_name="Indian Institute of Technology Bombay",
        courses=[
            Course(course_name="Thermodynamics", course_code="ME201", faculty="Dr. Anjali Mehta"),
            Course(course_name="Fluid Mechanics", course_code="ME202", faculty="Prof. Karan Singh"),
        ],
    ),
    "2024EC015": StudentRecord(
        roll_no="2024EC015",
        full_name="Priya Nambiar",
        college_name="National Institute of Technology Warangal",
        courses=[
            Course(course_name="Signals & Systems", course_code="EC401", faculty="Dr. Srinivas Rao"),
            Course(course_name="Digital Electronics", course_code="EC402", faculty="Prof. Deepa Krishnan"),
            Course(course_name="Microprocessors", course_code="EC403", faculty="Dr. Arun Pillai"),
        ],
    ),
}


# --------------------------------------------------------------------------- #
# GET Endpoints
# --------------------------------------------------------------------------- #

@app.get("/students", response_model=List[StudentRecord], summary="Get all student records")
def get_all_students():
    """
    Retrieve the complete list of student records, including their enrolled
    courses, course codes, and corresponding faculty.
    """
    return list(STUDENTS.values())


@app.get("/students/{roll_no}", response_model=StudentRecord, summary="Get a student by roll number")
def get_student_by_roll_no(roll_no: str):
    """
    Retrieve a single student record by their **roll number**.

    - **roll_no**: Unique roll number assigned to the student.
    """
    student = STUDENTS.get(roll_no)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with roll number '{roll_no}' not found.")
    return student


@app.get("/students/search/by-name", response_model=List[StudentRecord], summary="Search students by name")
def search_students_by_name(
    name: str = Query(..., min_length=2, description="Full or partial name to search for")
):
    """
    Search student records by **full name** (case-insensitive, partial match).
    """
    matches = [
        s for s in STUDENTS.values()
        if name.lower() in s.full_name.lower()
    ]
    if not matches:
        raise HTTPException(status_code=404, detail=f"No students found matching name '{name}'.")
    return matches


@app.get("/students/search/by-college", response_model=List[StudentRecord], summary="Search students by college")
def search_students_by_college(
    college: str = Query(..., min_length=2, description="College name to filter by")
):
    """
    Retrieve all student records belonging to a specific **college** (case-insensitive, partial match).
    """
    matches = [
        s for s in STUDENTS.values()
        if college.lower() in s.college_name.lower()
    ]
    if not matches:
        raise HTTPException(status_code=404, detail=f"No students found for college '{college}'.")
    return matches


@app.get("/students/search/by-course-code", response_model=List[StudentRecord], summary="Search students by course code")
def search_students_by_course_code(
    code: str = Query(..., min_length=2, description="Course code to search (e.g. CS301)")
):
    """
    Find all students enrolled in a course identified by its **course code**.
    """
    matches = [
        s for s in STUDENTS.values()
        if any(c.course_code.upper() == code.upper() for c in s.courses)
    ]
    if not matches:
        raise HTTPException(status_code=404, detail=f"No students found enrolled in course '{code}'.")
    return matches


@app.get("/students/{roll_no}/courses", response_model=List[Course], summary="Get courses for a student")
def get_courses_for_student(roll_no: str):
    """
    Retrieve the list of **courses**, their codes, and **faculty** for a specific student.
    """
    student = STUDENTS.get(roll_no)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with roll number '{roll_no}' not found.")
    return student.courses


# --------------------------------------------------------------------------- #
# Run with: uvicorn student_records:app --reload
# --------------------------------------------------------------------------- #