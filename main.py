from fastapi import FastAPI

from routers import auth , product , orders , review , customers , analytics

app = FastAPI()

app.include_router(prefix="/api", router=auth.router)
app.include_router(prefix="/api", router=product.router)
app.include_router(prefix="/api", router=orders.router)
app.include_router(prefix="/api", router=review.router)
app.include_router(prefix="/api", router=customers.router)
app.include_router(prefix="/api", router=analytics.router)

