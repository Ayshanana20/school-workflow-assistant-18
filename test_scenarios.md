# Project 18: Test Scenarios & Results

1. **Successful Student Lookup**: Request student record for `S001`. *Result*: Returns Aisha Bello's grade and class.
2. **Successful Course Info Search**: Request info for course code `ETEN301`. *Result*: Returns Circuit Theory policy details.
3. **Successful Grade Calculation**: Calculate weighted score with 80 and 90. *Result*: Returns calculated average score.
4. **Validation Error - Missing Field**: Send query to `/run-tool` omitting the `prompt` field. *Result*: Returns HTTP 422 error.
5. **Validation Error - Invalid Data Type**: Send string instead of float to `calculate_grade`. *Result*: Returns HTTP 422 error.
6. **Validation Error - Unknown Tool**: Request a tool name not defined in backend. *Result*: Returns HTTP 400 error.
7. **Sensitive Action - Grade Change Trigger**: Request `request_grade_change` for `S001`. *Result*: Halts execution, returns `PENDING_APPROVAL` token.
8. **Sensitive Action - Explicit Rejection**: Pass approval token to `/approve-action` with `approved: false`. *Result*: Returns rejection message; mock database remains unchanged.
9. **Sensitive Action - Explicit Approval**: Pass approval token to `/approve-action` with `approved: true`. *Result*: Updates mock database successfully and returns success status.
10. **Audit Log Verification**: Inspect console output during tool calls. *Result*: Logs successful actions and redacts sensitive parameters correctly.