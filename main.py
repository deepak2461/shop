from fastapi import FastAPI

from routers import auth

app = FastAPI()

app.include_router(prefix="/api", router=auth.router)
