from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.files import router as files_router


app = FastAPI(
    title="Secure File Platform API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(files_router)


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/health")
def health():
    return {"status": "ok"}