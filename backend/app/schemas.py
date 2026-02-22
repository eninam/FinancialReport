from pydantic import BaseModel #class validation
from typing import List, Dict, Optional, Literal

class SuggestedRange(BaseModel):
    min: float
    max: float

class JobStatus(BaseModel):
    pdfs_processed: int
    total_pdfs: int
    step: str
    errors: List[str] = []
    result: AnalysisResult

class CategorySummary(BaseModel):
    spent: float
    percentage_of_income: float
    delta_to_range: float
    status: Literal["under", "within", "over"]
    suggested_range: SuggestedRange

class AnalysisResult(BaseModel):
    average_monthly_income: float
    categories: Dict[str, CategorySummary]
    alerts: List[Alert]
    savings_suggestions: List[Suggestion]

class UploadResponse(BaseModel):
    job_id: str
    total_files: int
    status: str

class Suggestion(BaseModel):
    category: str
    action: str
    message: str
    amount: float

class Alert(BaseModel):
    category: str
    over_by: float
    message: str