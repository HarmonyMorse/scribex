from fastapi import FastAPI
from app.routers import users, auth

app = FastAPI(
    title="ScribeX API",
    description="ScribeX writing education platform API",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "database": "connected",
        "environment": "development"
    }

# Include routers with prefixes
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
