from fastapi import FastAPI

app = FastAPI(title="IA Dev Template")

@app.get("/health")
def health():
    return {"status": "ok"}
