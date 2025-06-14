from pydantic import BaseModel


class ApiResult(BaseModel):
    result: str  # e.g., "success" or "error"
    message: str  # A message describing the result of the operation
    kind: str # Type of response