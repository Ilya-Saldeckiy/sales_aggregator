from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import date
from models.sale import Sale, SaleBatchResponse
from services.storage import db

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("", response_model=SaleBatchResponse)
async def add_sales(sales: List[Sale]):
    count = db.add_sales(sales)
    return {"added_count": count}

@router.get("", response_model=List[Sale])
async def get_sales(
    marketplace: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    data = db.get_all()
    filtered = data
    if marketplace:
        filtered = [s for s in filtered if s.marketplace == marketplace]
    if status:
        filtered = [s for s in filtered if s.status == status]
    if date_from:
        filtered = [s for s in filtered if s.sold_at >= date_from]
    if date_to:
        filtered = [s for s in filtered if s.sold_at <= date_to]
    start = (page - 1) * page_size
    end = start + page_size
    return filtered[start:end]