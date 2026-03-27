from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.agent_monitor import router as monitor_router
from api.routes.analyze import router as analyze_router  

app = FastAPI(
    title="Risk Intelligence System",
    description="Distributed multi-agent business risk intelligence platform",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitor_router)
app.include_router(analyze_router)

@app.get("/")
def root():
    return {"message": "Risk Intelligence API running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
     