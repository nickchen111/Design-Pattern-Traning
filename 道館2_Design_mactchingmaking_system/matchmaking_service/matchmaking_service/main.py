from fastapi import FastAPI

app = FastAPI(title="Matchmaking Service")


@app.get("/")
def root():
    return {"status": "ok", "message": "Matchmaking Service is running."}
