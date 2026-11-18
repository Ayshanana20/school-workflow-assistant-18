from pydantic import BaseModel, Field
from typing import Optional

# Mock School Database
MOCK_STUDENTS = {
    "S001": {"name": "Aisha Bello", "grade": 88, "class": "Electrical Engineering 101"},
    "S002": {"name": "John Doe", "grade": 72, "class": "Circuit Theory"},
}

MOCK_COURSES = {
    "ETEN301": {"title": "Circuit Theory and Systems I", "policy": "Attendance is mandatory for all lab practicals."},
    "ETEN314": {"title": "Laboratory Practical Reports", "policy": "Reports must be submitted within 48 hours of experiment completion."},
}

# Pydantic Schemas for Tool Validation
class SearchInput(BaseModel):
    course_code: str = Field(..., description="The course code to look up (e.g., ETEN301)")

class GradeCalculatorInput(BaseModel):
    score1: float
    score2: float
    weight1: float = 0.5
    weight2: float = 0.5

class StudentRecordInput(BaseModel):
    student_id: str = Field(..., description="Student ID number (e.g., S001)")

class SensitiveGradeChangeInput(BaseModel):
    student_id: str
    new_grade: float
    reason: str

# Tool Functions
def search_school_info(course_code: str) -> dict:
    """Find class, course, or policy information."""
    return MOCK_COURSES.get(course_code.upper(), {"error": "Course not found."})

def calculate_grade(score1: float, score2: float, weight1: float, weight2: float) -> dict:
    """Calculate a weighted average score."""
    final_score = (score1 * weight1) + (score2 * weight2)
    return {"calculated_average": round(final_score, 2)}

def lookup_student_record(student_id: str) -> dict:
    """Retrieve a student record from the mock database."""
    return MOCK_STUDENTS.get(student_id.upper(), {"error": "Student record not found."})

def request_grade_change(student_id: str, new_grade: float, reason: str) -> dict:
    """Sensitive action: Prepare a request to change a student's grade."""
    if student_id.upper() not in MOCK_STUDENTS:
        return {"error": "Student not found."}
    
    # Returns a pending sensitive action structure requiring manual approval
    return {
        "status": "PENDING_APPROVAL",
        "action": "CHANGE_GRADE",
        "student_id": student_id.upper(),
        "target_student": MOCK_STUDENTS[student_id.upper()]["name"],
        "old_grade": MOCK_STUDENTS[student_id.upper()]["grade"],
        "proposed_grade": new_grade,
        "reason": reason,
        "message": "⚠️ SENSITIVE ACTION: Explicit authorization required before database write."
    }