from decimal import Decimal

from pydantic import BaseModel, Field


class RefundRequest(BaseModel):
    order_id: int
    reason: str = Field(min_length=10)
    refund_amount: Decimal = Field(gt=0)
