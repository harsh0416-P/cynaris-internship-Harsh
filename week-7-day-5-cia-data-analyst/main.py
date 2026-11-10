
import io
import uuid
import logging
from pathlib import Path

import pandas as pd

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from csv_analyzer import CSVAnalyzer


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
STATIC_DIR = BASE_DIR / "static"

UPLOAD_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CIA-Data-Analyst")


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Cynaris CIA Data Analyst",
    description="AI-powered CSV Data Analysis using PandasAI",
    version="1.1.0"
)


# Temporary in-memory dataset sessions
datasets = {}


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class AnalysisRequest(BaseModel):
    session_id: str
    question: str


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "running",
        "application": "Cynaris CIA Data Analyst",
        "model": "llama3.2:3b",
        "active_sessions": len(datasets)
    }


# --------------------------------------------------
# CSV UPLOAD
# --------------------------------------------------

@app.post("/cia/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    if not file.filename or Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    try:
        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="CSV file exceeds the 20 MB limit."
            )

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        df = pd.read_csv(io.BytesIO(content))

        if df.empty or len(df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="CSV contains no usable data."
            )

        if len(df.columns) > 200:
            raise HTTPException(
                status_code=400,
                detail="CSV has too many columns."
            )

        session_id = str(uuid.uuid4())

        analyzer = CSVAnalyzer(df)

        datasets[session_id] = {
            "analyzer": analyzer,
            "filename": Path(file.filename).name,
            "rows": len(df),
            "columns": len(df.columns)
        }

        logger.info(
            "Dataset uploaded: %s | Rows: %s",
            file.filename,
            len(df)
        )

        return {
            "success": True,
            "session_id": session_id,
            "filename": Path(file.filename).name,
            "rows": len(df),
            "columns": len(df.columns),
            "dataset_info": analyzer.get_dataset_info()
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("CSV upload failed")

        raise HTTPException(
            status_code=400,
            detail=f"Unable to process CSV: {str(error)}"
        )

    finally:
        await file.close()


# --------------------------------------------------
# DATASET INFORMATION
# --------------------------------------------------

@app.get("/cia/dataset-info/{session_id}")
async def dataset_info(session_id: str):

    dataset = datasets.get(session_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset session not found."
        )

    return dataset["analyzer"].get_dataset_info()


# --------------------------------------------------
# AI DATA ANALYSIS
# --------------------------------------------------

@app.post("/cia/analyze")
async def analyze_data(request: AnalysisRequest):

    dataset = datasets.get(request.session_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Upload a CSV file before asking questions."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = dataset["analyzer"].analyze(request.question)

        return {
            "success": True,
            "filename": dataset["filename"],
            **result
        }

    except Exception as error:
        logger.exception("Analysis failed")

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(error)}"
        )


# --------------------------------------------------
# FRONTEND STATIC FILES
# Keep this mount LAST so API routes work.
# --------------------------------------------------

app.mount(
    "/",
    StaticFiles(directory=str(STATIC_DIR), html=True),
    name="frontend"
)
