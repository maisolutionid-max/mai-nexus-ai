from fastapi import FastAPI

app = FastAPI(
    title="MAI Nexus AI",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to MAI Nexus AI Laundry Module"
    }
