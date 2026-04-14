from pydantic import BaseModel
from typing import List, Optional

class SummaryMetrics(BaseModel):
    group: Optional[str] = None
    total_revenue: float
    total_cost: float
    gross_profit: float
    margin_percent: float
    total_orders: int
    avg_order_value: float
    return_rate: float

class CSVUploadResponse(BaseModel):
    total_rows: int
    error_count: int
    errors: List[str]