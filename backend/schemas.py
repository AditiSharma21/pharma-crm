from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional



# Medicine Schemas


class MedicineCreate(BaseModel):
    name: str
    generic_name: str
    manufacturer: str
    batch_no: str
    expiry_date: date
    quantity: int
    price: float


class MedicineResponse(BaseModel):
    id: int
    name: str
    generic_name: str
    manufacturer: str
    batch_no: str
    expiry_date: date
    quantity: int
    price: float
    status: str

    class Config:
        from_attributes = True



# Sale Schemas


class SaleCreate(BaseModel):
    medicine_id: int
    quantity_sold: int


class SaleResponse(BaseModel):
    id: int
    medicine_id: int
    quantity_sold: int
    total_amount: float
    sold_at: datetime

    class Config:
        from_attributes = True



# Purchase Order Schemas


class PurchaseCreate(BaseModel):
    supplier_name: str
    total_amount: float


class PurchaseResponse(BaseModel):
    id: int
    supplier_name: str
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True