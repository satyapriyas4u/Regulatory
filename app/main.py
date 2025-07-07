# File: app/main.py
# This file is the entry point for the FastAPI application.


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from regulatory import LONG_DESCRIPTION, __version__ as VERSION
from app.api.routes import router

app = FastAPI(
    title="Regulatory AI Backend Core API",
    version=str(VERSION),
    description=LONG_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS (allow all origins for now; update for production use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount a folder called "static" at the "/static" path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root Endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="""**Returns a simple welcome page.**""",
    response_class=FileResponse,
)
async def root():
    return FileResponse("static/index.html")

app.include_router(router)

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
# To run the application, use the command:
# uvicorn app.main:app --host
# uv run -m app.main

# Note: The above line is for development purposes. In production, use a proper ASGI server like Gunicorn or Uvicorn with a process manager.
# Example: gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --workers 4
