from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base



# Medicine Model

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    generic_name = Column(String)
    manufacturer = Column(String)
    batch_no = Column(String)
    expiry_date = Column(Date)
    quantity = Column(Integer)
    price = Column(Float)
    status = Column(String)

    sales = relationship("Sale", back_populates="medicine")



# Sale Model

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    quantity_sold = Column(Integer)
    total_amount = Column(Float)
    sold_at = Column(DateTime, default=datetime.utcnow)

    medicine = relationship("Medicine", back_populates="sales")



# Purchase Order Model

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String)
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)