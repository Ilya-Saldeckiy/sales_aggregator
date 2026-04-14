from fastapi import APIRouter, UploadFile, File
from datetime import date
from typing import List, Optional
import pandas as pd
import io
from models.sale import Sale
from models.analytics import SummaryMetrics, CSVUploadResponse
from services.storage import db
from services.aggregation import get_summary
from services.currency import currency_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary", response_model=List[SummaryMetrics])
async def summary(date_from: date, date_to: date, marketplace: Optional[str] = None, group_by: Optional[str] = None):
    return get_summary(db.get_all(), date_from, date_to, marketplace, group_by)

@router.get("/summary-usd", response_model=List[SummaryMetrics])
async def summary_usd(date_from: date, date_to: date, marketplace: Optional[str] = None, group_by: Optional[str] = None):
    res = get_summary(db.get_all(), date_from, date_to, marketplace, group_by)
    rate = await currency_service.get_usd_rate()
    for item in res:
        item["total_revenue"] = round(item["total_revenue"] / rate, 2)
        item["total_cost"] = round(item["total_cost"] / rate, 2)
        item["gross_profit"] = round(item["gross_profit"] / rate, 2)
        item["avg_order_value"] = round(item["avg_order_value"] / rate, 2)
    return res

@router.post("/upload-csv", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    valid_sales, errors = [], []
    for index, row in df.iterrows():
        try:
            sale = Sale(**row.to_dict())
            valid_sales.append(sale)
        except Exception as e:
            errors.append(f"Row {index + 1}: {str(e)}")
    db.add_sales(valid_sales)
    return {"total_rows": len(df), "error_count": len(errors), "errors": errors}