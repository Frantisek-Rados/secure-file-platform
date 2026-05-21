from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Secure File Platform API"}