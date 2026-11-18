# School Support Workflow Assistant (Project 18)

An AI assistant backend featuring tool selection, Pydantic validation, mock database integration, audit logging, and a sensitive-action approval/rejection flow built with FastAPI.

## Features
- **Tool-Using Assistant:** Supports student record lookup, course search, grade calculations, and grade modifications.
- **Pydantic Validation:** Validates input parameters and catches malformed queries before execution.
- **Safety Boundary:** Halts sensitive write operations (`request_grade_change`) and requires explicit manual approval.
- **Audit Logging:** Records execution metadata with sensitive data sanitized.

## Setup & Usage
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt