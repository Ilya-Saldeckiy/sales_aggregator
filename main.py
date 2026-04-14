from fastapi import FastAPI
from routers import sales, analytics
from logger import logger

app = FastAPI(title="Marketplace Sales Aggregator API")

app.include_router(sales.router)
app.include_router(analytics.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Сервис агрегации продаж запущен")

@app.get("/")
async def root():
    return {"message": "API is running. Go to /docs for documentation."}