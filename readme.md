## Description

## Backend

    User uploads PDF
            ↓
    python-multipart parses request
            ↓
    FastAPI receives UploadFile
            ↓
    pdfplumber extracts text (locally)
            ↓
    pydantic validates parsed data
            ↓
    Rules + analysis generate insights
            ↓
    Only insights returned / stored

## Front End

npm run start

## Todo

    python3  -m uvicorn main:app --reload
    python3 -m pip install packageName
    npm start
    deploy backend to web
    deploy front end to web
    add a database layer for categorization
    add a database layer parsed statements data
    add a database layer analysis of statement data
    allow the user to input their own suggested percentage categories on front end
    add ai for statement analysis
