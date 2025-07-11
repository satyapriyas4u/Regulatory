

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

from regulatory import LONG_DESCRIPTION, __version__ as VERSION
from app.api.routes import router
from src.regulatory.graph.workflow import run_workflow_from_input

app = FastAPI(
    title="Regulatory AI Backend Core API",
    version=str(VERSION),
    description=LONG_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ----------------------------- Enable CORS -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------- Static File Serving -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------- Root Endpoint -----------------------------
@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Returns a simple welcome message for the Regulatory AI Backend.",
    response_class=FileResponse,
)
async def root():
    return FileResponse("static/index.html")

# ----------------------------- GSPR Input Schema -----------------------------
class DeviceInput(BaseModel):
    device_type: str
    intended_use: str
    intended_users: Optional[List[str]]
    components: List[str]
    region_classification: str

# ----------------------------- GSPR Generation Route -----------------------------
@app.post("/generate-gspr", tags=["GSPR"])
async def generate_gspr(input_data: DeviceInput):
    try:
        result = run_workflow_from_input(input_data.dict())
        return {"status": "success", "gspr_report": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------- API Routes -----------------------------
app.include_router(router)

# ----------------------------- Local Development Entry Point -----------------------------
if __name__ == "__main__":
    import uvicorn
    from regulatory.utils.logger import log_config

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8580,
        reload=True,
        log_config=log_config,
        log_level="info"
    )
