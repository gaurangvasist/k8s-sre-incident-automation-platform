from fastapi import FastAPI


app = FastAPI(title="Cloud Native GitOps Platform")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
