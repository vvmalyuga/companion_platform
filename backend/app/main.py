from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router
from backend.app.core.logging import configureLogging
from backend.app.infra.database import initDb

configureLogging()

app = FastAPI(title="Companion Platform API", version="1.0.0", description="Operational API and event source for the Companion data platform.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")


@app.on_event("startup")
def startup() -> None:
    initDb()
