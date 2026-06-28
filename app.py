from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

EMAIL = "23f1000190@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-92b34o.example.com"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start
        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response

app.add_middleware(HeadersMiddleware)

@app.get("/stats")
async def stats(values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
