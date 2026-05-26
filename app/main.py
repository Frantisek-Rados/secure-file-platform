from fastapi import FastAPI
from app.routes import auth, files
from app.core.database import Base, engine

app = FastAPI(title="Secure File Platform")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(files.router)


@app.get("/")
def root():
    return {"message": "Secure File Platform API"}