from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os

# --------------------------------------------------------------------------- #
# App setup
# --------------------------------------------------------------------------- #

app = FastAPI(
    title="Student Records CRUD API",
    description="Full CRUD API for managing student records using MongoDB",
    version="2.0.0",
)

# --------------------------------------------------------------------------- #
# MongoDB connection — your existing setup
# --------------------------------------------------------------------------- #

import urllib.parse

username = "Anish"
password = urllib.parse.quote_plus("Anish@0202")  # encodes @ as %40

MONGO_DETAILS = os.getenv(
    "MONGO_URI",
    f"mongodb+srv://{username}:{password}@cluster0.dgkgee4.mongodb.net/?appName=Cluster0"
)

client     = MongoClient(MONGO_DETAILS)
db         = client.genai
collection = db.students          # using 'students' collection inside 'genai' db


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def serialize(doc: dict) -> dict:
    """Replace ObjectId with a plain string so JSON can handle it."""
    doc["id"] = str(doc.pop("_id"))
    return doc


def valid_object_id(oid: str) -> ObjectId:
    """Convert string to ObjectId; raise 400 if the format is invalid."""
    try:
        return ObjectId(oid)
    except (InvalidId, Exception):
        raise HTTPException(status_code=400, detail=f"'{oid}' is not a valid MongoDB ObjectId.")


# --------------------------------------------------------------------------- #
# Pydantic models
# --------------------------------------------------------------------------- #

class Course(BaseModel):
    course_name: str = Field(..., example="Data Structures")
    course_code: str = Field(..., example="CS301")
    faculty:     str = Field(..., example="Dr. Ramesh Kumar")


class StudentCreate(BaseModel):
    roll_no:      str          = Field(..., example="2024CS001")
    full_name:    str          = Field(..., example="Aanya Sharma")
    college_name: str          = Field(..., example="NIT Warangal")
    courses:      List[Course] = Field(..., min_items=1)


class StudentUpdate(BaseModel):
    full_name:    Optional[str]          = None
    college_name: Optional[str]          = None
    courses:      Optional[List[Course]] = None


class StudentResponse(StudentCreate):
    id: str


# --------------------------------------------------------------------------- #
# CREATE — POST /students
# --------------------------------------------------------------------------- #

@app.post("/students", response_model=StudentResponse, status_code=201,
          summary="Create a new student record")
def create_student(student: StudentCreate):
    existing = collection.find_one({"roll_no": student.roll_no})
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"A student with roll number '{student.roll_no}' already exists."
        )
    doc    = student.model_dump()
    result = collection.insert_one(doc)
    created = collection.find_one({"_id": result.inserted_id})
    return serialize(created)


# --------------------------------------------------------------------------- #
# READ — GET /students
# --------------------------------------------------------------------------- #

@app.get("/students", response_model=List[StudentResponse],
         summary="Get all student records")
def get_all_students(
    skip:  int = Query(0,  ge=0,         description="Records to skip (pagination)"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return (1-100)")
):
    students = list(collection.find().skip(skip).limit(limit))
    return [serialize(s) for s in students]


# --------------------------------------------------------------------------- #
# READ — GET /students/{id}
# --------------------------------------------------------------------------- #

@app.get("/students/{id}", response_model=StudentResponse,
         summary="Get a student by MongoDB id")
def get_student(id: str = Path(..., description="MongoDB ObjectId")):
    student = collection.find_one({"_id": valid_object_id(id)})
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id '{id}' not found.")
    return serialize(student)


# --------------------------------------------------------------------------- #
# READ — GET /students/roll/{roll_no}
# --------------------------------------------------------------------------- #

@app.get("/students/roll/{roll_no}", response_model=StudentResponse,
         summary="Get a student by roll number")
def get_student_by_roll(roll_no: str):
    student = collection.find_one({"roll_no": roll_no})
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{roll_no}' not found.")
    return serialize(student)


# --------------------------------------------------------------------------- #
# SEARCH endpoints
# --------------------------------------------------------------------------- #

@app.get("/students/search/by-name", response_model=List[StudentResponse],
         summary="Search students by name")
def search_by_name(
    name: str = Query(..., min_length=2, description="Partial or full name (case-insensitive)")
):
    students = list(collection.find({"full_name": {"$regex": name, "$options": "i"}}))
    if not students:
        raise HTTPException(status_code=404, detail=f"No students found matching '{name}'.")
    return [serialize(s) for s in students]


@app.get("/students/search/by-college", response_model=List[StudentResponse],
         summary="Search students by college")
def search_by_college(
    college: str = Query(..., min_length=2, description="Partial or full college name")
):
    students = list(collection.find({"college_name": {"$regex": college, "$options": "i"}}))
    if not students:
        raise HTTPException(status_code=404, detail=f"No students found for college '{college}'.")
    return [serialize(s) for s in students]


@app.get("/students/search/by-course-code", response_model=List[StudentResponse],
         summary="Search students by course code")
def search_by_course_code(
    code: str = Query(..., min_length=2, description="Exact course code e.g. CS301")
):
    students = list(collection.find({"courses.course_code": {"$regex": f"^{code}$", "$options": "i"}}))
    if not students:
        raise HTTPException(status_code=404, detail=f"No students enrolled in course '{code}'.")
    return [serialize(s) for s in students]


# --------------------------------------------------------------------------- #
# UPDATE — PUT /students/{id}
# --------------------------------------------------------------------------- #

@app.put("/students/{id}", response_model=StudentResponse,
         summary="Fully replace a student record")
def replace_student(
    id:      str           = Path(..., description="MongoDB ObjectId"),
    student: StudentCreate = ...
):
    result = collection.find_one_and_replace(
        {"_id": valid_object_id(id)},
        student.model_dump(),
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail=f"Student with id '{id}' not found.")
    return serialize(result)


# --------------------------------------------------------------------------- #
# UPDATE — PATCH /students/{id}
# --------------------------------------------------------------------------- #

@app.patch("/students/{id}", response_model=StudentResponse,
           summary="Partially update a student record")
def update_student(
    id:     str           = Path(..., description="MongoDB ObjectId"),
    update: StudentUpdate = ...
):
    changes = {k: v for k, v in update.model_dump().items() if v is not None}
    if not changes:
        raise HTTPException(status_code=422, detail="No fields provided to update.")

    if "courses" in changes:
        changes["courses"] = [
            c.model_dump() if hasattr(c, "model_dump") else c
            for c in changes["courses"]
        ]

    result = collection.find_one_and_update(
        {"_id": valid_object_id(id)},
        {"$set": changes},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail=f"Student with id '{id}' not found.")
    return serialize(result)


# --------------------------------------------------------------------------- #
# DELETE — DELETE /students/{id}
# --------------------------------------------------------------------------- #

@app.delete("/students/{id}", status_code=200,
            summary="Delete a student record")
def delete_student(id: str = Path(..., description="MongoDB ObjectId")):
    result = collection.delete_one({"_id": valid_object_id(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Student with id '{id}' not found.")
    return {"message": f"Student '{id}' deleted successfully."}


# --------------------------------------------------------------------------- #
# DELETE — DELETE /students/roll/{roll_no}
# --------------------------------------------------------------------------- #

@app.delete("/students/roll/{roll_no}", status_code=200,
            summary="Delete a student by roll number")
def delete_student_by_roll(roll_no: str):
    result = collection.delete_one({"roll_no": roll_no})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Student '{roll_no}' not found.")
    return {"message": f"Student '{roll_no}' deleted successfully."}


# --------------------------------------------------------------------------- #
# Health check
# --------------------------------------------------------------------------- #

@app.get("/health", tags=["Meta"], summary="Health check")
def health():
    db.command("ping")
    return {"status": "ok", "database": "genai", "collection": "students"}


# --------------------------------------------------------------------------- #
# Run with:  uvicorn student_records:app --reload
# --------------------------------------------------------------------------- #