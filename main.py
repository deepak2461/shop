from fastapi import FastAPI

from routers import auth , product

app = FastAPI()

app.include_router(prefix="/api", router=auth.router)
app.include_router(prefix="/api", router=product.router)

