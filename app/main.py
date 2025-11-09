from fastapi import FastAPI

from app.routers.prompt_service import router as prompt_router

app = FastAPI(title="Prompt Service")

app.include_router(prompt_router, prefix="/api/v1")
