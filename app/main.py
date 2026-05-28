from fastapi import FastAPI
from app.routes import auth, files

app = FastAPI(
    title="Secure File Platform API",
    description="Secure backend for file upload and management",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
def root():
    return {
        "message": "Secure File Platform API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }