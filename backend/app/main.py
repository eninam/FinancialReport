from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from uuid import uuid4
from typing import List
from store import job_store, lock
from pdf_parser import extract_statement_data
from analysis import analyze_spending
from schemas import JobStatus, UploadResponse
from fastapi.middleware.cors import CORSMiddleware
# from upload_routes import router  # or wherever your endpoints are

app = FastAPI(title="PDF Finance Analyzer")

MIN_PDFS = 1
MAX_PDFS = 12

app = FastAPI()

# Allow requests from Angular dev server
origins = [
    "http://localhost:4200",
    # add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],     # allow POST, GET, etc
    allow_headers=["*"],
)

# include your routes
# app.include_router(router)

@app.post("/upload",response_model=UploadResponse)
async def upload_pdfs(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    print("files")
    print(files)
    if not (MIN_PDFS <= len(files) <= MAX_PDFS):
        raise HTTPException(400, "Upload between 2 and 12 PDFs")

    job_id = str(uuid4())
    with lock:
        job_store[job_id] = {
            "pdfs_processed": 0,
            "total_pdfs": len(files),
            "step": "Starting",
            "errors": [],
            "result": None
        }

    background_tasks.add_task(process_job, job_id, files)
    print("UploadResponse sent to fe" , UploadResponse(  
        job_id=job_id,
        total_files=len(files),
        status="processing"
    ))
    return UploadResponse(  
        job_id=job_id,
        total_files=len(files),
        status="processing"
    )
def process_job(job_id: str, files: List[UploadFile]):
    statements = [] # will looks something like [{income:3.4, transactions:[]},{...}] , each object is a parsed statment

    for f in files:
        try:
            pdf_bytes = f.file
            # extracts the income and transactions of a given file
            data = extract_statement_data(pdf_bytes)
            statements.append(data)

            with lock:
                job_store[job_id]["pdfs_processed"] += 1
                job_store[job_id]["step"] = (
                    f"Processed {job_store[job_id]['pdfs_processed']} of "
                    f"{job_store[job_id]['total_pdfs']} PDFs"
                )
        except Exception as e:
            with lock:
                job_store[job_id]["errors"].append(str(e))

    if len(statements) >= MIN_PDFS:
        avg_income, categories, alerts, suggestions = analyze_spending(statements)

        with lock:
            job_store[job_id]["result"] = {
                "average_monthly_income": avg_income,
                "categories": categories,
                "alerts": alerts,
                "savings_suggestions": suggestions
            }
            job_store[job_id]["step"] = "Analysis complete"

@app.get("/status/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return JobStatus(
        job_id=job_id,
        pdfs_processed=job["pdfs_processed"],
        result=job["result"],
        total_pdfs=job["total_pdfs"],
        errors=job["errors"],
        step=job["step"],
    )
