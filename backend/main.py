import logging
import os

import pymysql
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.users import router as users_router

load_dotenv()
logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="User Management API", version="1.0.0")

origins = os.getenv(
    "CORS_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)

@app.exception_handler(pymysql.MySQLError)
async def database_error_handler(request: Request, exc: pymysql.MySQLError):
    """Any unexpected MySQL problem becomes a clean JSON 500 response."""
    logger.error("Database error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Please try again later."},
    )



@app.get("/", tags=["Health"])
def root():
    return {"message": "User Management API is running. Open /docs for Swagger UI."}
