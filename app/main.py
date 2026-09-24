from fastapi import FastAPI

from .database import Base, engine

from .routers import (
    auth_router,
    problems,
    submissions,
    users
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="CodeArena",
    description="LeetCode-style coding practice platform",
    version="1.0.0"
)


app.include_router(
    auth_router.router
)

app.include_router(
    problems.router
)

app.include_router(
    submissions.router
)

app.include_router(
    users.router
)


@app.get("/")
def home():

    return {
        "message": "Welcome to CodeArena"
    }


@app.get("/health")
def health():

    return {
        "status": "OK"
    }