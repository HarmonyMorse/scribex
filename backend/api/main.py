from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import users, auth
from app.core.config import settings

app = FastAPI(
    title="ScribeX API",
    description="ScribeX writing education platform API",
    version="0.1.0"
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/health", tags=["health"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "version": app.version,
            "database": "connected" if settings.DATABASE_URL else "not configured",
            "environment": "development"
        }
    ) 