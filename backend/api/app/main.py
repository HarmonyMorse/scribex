from fastapi import FastAPI
from app.routers import users, auth

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "database": "connected",
        "environment": "development"
    }

# Include routers
app.include_router(users.router)
app.include_router(auth.router) 