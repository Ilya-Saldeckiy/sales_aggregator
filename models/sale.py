from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import date

class Sale(BaseModel):
    order_id: str
    marketplace: Literal["ozon", "wildberries", "yandex_market"]
    product_name: str
    quantity: int = Field(..., ge=1)
    price: float = Field(..., gt=0)
    cost_price: float = Field(..., gt=0)
    status: Literal["delivered", "returned", "cancelled"]
    sold_at: date

    @field_validator("sold_at")
    @classmethod
    def date_not_in_future(cls, v):
        if v > date.today():
            raise ValueError("Дата не может быть в будущем")
        return v

class SaleBatchResponse(BaseModel):
    added_count: int