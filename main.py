from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from tools import (
    search_school_info,
    calculate_grade,
    lookup_student_record,
    request_grade_change,
    SearchInput,
    GradeCalculatorInput,
    StudentRecordInput,
    SensitiveGradeChangeInput
)

app = FastAPI(title="School Support Workflow Assistant API")

class UserQuery(BaseModel):
    prompt: str
    tool_name: str
    arguments: dict

class ApprovalRequest(BaseModel):
    action_token: dict
    approved: bool

# Audit Logger helper with sensitive data masking
def log_audit_event(tool_name: str, arguments: dict, status: str):
    timestamp = datetime.datetime.now().isoformat()
    # Mask sensitive fields if present
    sanitized_args = arguments.copy()
    if "new_grade" in sanitized_args:
        sanitized_args["new_grade"] = "[REDACTED]"
    
    print(f"[AUDIT LOG] {timestamp} | Tool: {tool_name} | Args: {sanitized_args} | Status: {status}")

@app.get("/")
def home():
    return {"message": "School Support Assistant API is running with tool-calling and safety boundaries!"}

@app.post("/run-tool")
def run_tool(query: UserQuery):
    """Selects and executes tools with Pydantic validation."""
    tool = query.tool_name
    args = query.arguments

    try:
        if tool == "search_school_info":
            validated_args = SearchInput(**args)
            result = search_school_info(**validated_args.model_dump())
            log_audit_event(tool, args, "SUCCESS")
            return {"result": result}
        
        elif tool == "calculate_grade":
            validated_args = GradeCalculatorInput(**args)
            result = calculate_grade(**validated_args.model_dump())
            log_audit_event(tool, args, "SUCCESS")
            return {"result": result}
        
        elif tool == "lookup_student":
            validated_args = StudentRecordInput(**args)
            result = lookup_student_record(**validated_args.model_dump())
            log_audit_event(tool, args, "SUCCESS")
            return {"result": result}
        
        elif tool == "request_grade_change":
            validated_args = SensitiveGradeChangeInput(**args)
            pending_action = request_grade_change(**validated_args.model_dump())
            log_audit_event(tool, args, "PENDING_APPROVAL")
            return {
                "requires_approval": True,
                "pending_action": pending_action
            }
        
        else:
            log_audit_event(tool, args, "UNKNOWN_TOOL")
            raise HTTPException(status_code=400, detail="Unknown tool requested.")
            
    except Exception as e:
        log_audit_event(tool, args, "VALIDATION_ERROR")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")

@app.post("/approve-action")
def approve_action(approval: ApprovalRequest):
    """Enforces approval and rejection flow for sensitive actions."""
    if not approval.approved:
        log_audit_event("approve_action", {"action": "CHANGE_GRADE"}, "REJECTED")
        return {"status": "REJECTED", "message": "Action was explicitly rejected by user/admin. No changes were made."}
    
    action_data = approval.action_token
    if action_data.get("action") == "CHANGE_GRADE":
        student_id = action_data["student_id"]
        new_grade = action_data["proposed_grade"]
        
        from tools import MOCK_STUDENTS
        MOCK_STUDENTS[student_id]["grade"] = new_grade
        
        log_audit_event("approve_action", {"student_id": student_id}, "SUCCESS")
        return {
            "status": "SUCCESS",
            "message": f"Successfully updated grade for {action_data['target_student']} to {new_grade}.",
            "updated_record": MOCK_STUDENTS[student_id]
        }
    
    raise HTTPException(status_code=400, detail="Invalid action token.")