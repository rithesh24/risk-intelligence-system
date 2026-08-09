import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routes.agent_monitor import router as monitor_router
from api.routes.analyze import router as analyze_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Risk Intelligence System",
    description="Distributed multi-agent business risk intelligence platform",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitor_router)
app.include_router(analyze_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Registered via FastAPI so it runs inside CORSMiddleware — without this,
    # an unhandled exception skips CORS headers entirely and the browser just
    # reports a generic "Failed to fetch", which looks like the whole app died.
    logger.exception(f"Unhandled error on {request.method} {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."},
    )

@app.get("/")
def root():
    return {"message": "Risk Intelligence API running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
     