"""Эталонная модель заказа на Pydantic v2 для проекта order-processor-lab."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderStatus(StrEnum):
    NEW = "new"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    sku: str = Field(min_length=3, max_length=32, description="Артикул товара")
    quantity: int = Field(gt=0, le=1000, description="Количество единиц")
    unit_price: Decimal = Field(gt=0, decimal_places=2, description="Цена за единицу")

    @field_validator("sku")
    @classmethod
    def sku_must_be_uppercase(cls, value: str) -> str:
        if not value.isalnum() or value != value.upper():
            raise ValueError(
                "Артикул должен состоять из заглавных латинских букв и цифр"
            )
        return value


class Order(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    order_id: int = Field(gt=0, description="Уникальный идентификатор заказа")
    customer_email: str = Field(min_length=5, max_length=254)
    items: list[OrderItem] = Field(min_length=1)
    status: OrderStatus = OrderStatus.NEW
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("customer_email")
    @classmethod
    def email_must_contain_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email клиента должен содержать символ '@'")
        return value.lower()

    @property
    def total(self) -> Decimal:
        return sum((i.unit_price * i.quantity for i in self.items), Decimal(0))
