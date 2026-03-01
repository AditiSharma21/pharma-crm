from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from datetime import datetime, date
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# INVENTORY APIs


# Create Medicine
@app.post("/inventory", response_model=schemas.MedicineResponse, status_code=201)
def create_medicine(medicine: schemas.MedicineCreate, db: Session = Depends(get_db)):

    status = "Active"
    if medicine.quantity == 0:
        status = "Out of Stock"
    elif medicine.quantity < 10:
        status = "Low Stock"

    db_medicine = models.Medicine(
        name=medicine.name,
        generic_name=medicine.generic_name,
        manufacturer=medicine.manufacturer,
        batch_no=medicine.batch_no,
        expiry_date=medicine.expiry_date,
        quantity=medicine.quantity,
        price=medicine.price,
        status=status
    )

    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    return db_medicine


# Get Inventory with Search + Filter
@app.get("/inventory", response_model=List[schemas.MedicineResponse])
def get_inventory(search: str = None, status: str = None, db: Session = Depends(get_db)):

    query = db.query(models.Medicine)

    if search:
        query = query.filter(models.Medicine.name.contains(search))

    medicines = query.all()

    # 🔥 Dynamic Status Auto-Detection
    for medicine in medicines:
        if medicine.quantity == 0:
            medicine.status = "Out of Stock"
        elif medicine.quantity < 10:
            medicine.status = "Low Stock"
        else:
            medicine.status = "Active"

    # Optional status filtering AFTER dynamic update
    if status:
        medicines = [m for m in medicines if m.status == status]

    return medicines


# Update Medicine
@app.put("/inventory/{medicine_id}", response_model=schemas.MedicineResponse)
def update_medicine(medicine_id: int, updated: schemas.MedicineCreate, db: Session = Depends(get_db)):

    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    medicine.name = updated.name
    medicine.generic_name = updated.generic_name
    medicine.manufacturer = updated.manufacturer
    medicine.batch_no = updated.batch_no
    medicine.expiry_date = updated.expiry_date
    medicine.quantity = updated.quantity
    medicine.price = updated.price

    # Recalculate status
    if medicine.quantity == 0:
        medicine.status = "Out of Stock"
    elif medicine.quantity < 10:
        medicine.status = "Low Stock"
    else:
        medicine.status = "Active"

    db.commit()
    db.refresh(medicine)

    return medicine


# Delete Medicine
@app.delete("/inventory/{medicine_id}", status_code=204)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):

    medicine = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    db.delete(medicine)
    db.commit()

    return {"message": "Deleted successfully"}



# SALES APIs


@app.post("/sales", response_model=schemas.SaleResponse, status_code=201)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):

    medicine = db.query(models.Medicine).filter(models.Medicine.id == sale.medicine_id).first()

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    if medicine.quantity < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Reduce stock
    medicine.quantity -= sale.quantity_sold

    # Update status automatically
    if medicine.quantity == 0:
        medicine.status = "Out of Stock"
    elif medicine.quantity < 10:
        medicine.status = "Low Stock"
    else:
        medicine.status = "Active"

    total_amount = sale.quantity_sold * medicine.price

    db_sale = models.Sale(
        medicine_id=sale.medicine_id,
        quantity_sold=sale.quantity_sold,
        total_amount=total_amount,
        sold_at=datetime.utcnow()
    )

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    return db_sale


# PURCHASE ORDER APIs


@app.post("/purchase-orders", response_model=schemas.PurchaseResponse, status_code=201)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):

    db_purchase = models.PurchaseOrder(
        supplier_name=purchase.supplier_name,
        total_amount=purchase.total_amount,
        created_at=datetime.utcnow()
    )

    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)

    return db_purchase


@app.get("/purchase-orders", response_model=List[schemas.PurchaseResponse])
def get_purchase_orders(db: Session = Depends(get_db)):
    return db.query(models.PurchaseOrder).all()



# DASHBOARD APIs


# Today's Sales
@app.get("/dashboard/today-sales")
def today_sales(db: Session = Depends(get_db)):

    today = datetime.utcnow().date()
    sales = db.query(models.Sale).all()

    total = 0
    transactions = 0

    for s in sales:
        if s.sold_at.date() == today:
            total += s.total_amount
            transactions += 1

    return {
        "total": total,
        "transactions": transactions
    }


# Total Items Sold
@app.get("/dashboard/total-items-sold")
def total_items_sold(db: Session = Depends(get_db)):

    sales = db.query(models.Sale).all()
    total_items = sum(s.quantity_sold for s in sales)

    return {"total_items_sold": total_items}


# Low Stock Medicines
@app.get("/dashboard/low-stock")
def low_stock(db: Session = Depends(get_db)):

    medicines = db.query(models.Medicine).filter(
        models.Medicine.quantity < 10,
        models.Medicine.quantity > 0
    ).all()

    return medicines


# Recent Sales
@app.get("/dashboard/recent-sales")
def recent_sales(db: Session = Depends(get_db)):

    sales = db.query(models.Sale).order_by(
        models.Sale.sold_at.desc()
    ).limit(5).all()

    return sales


# Purchase Summary
@app.get("/dashboard/purchase-summary")
def purchase_summary(db: Session = Depends(get_db)):

    purchases = db.query(models.PurchaseOrder).all()
    total = sum(p.total_amount for p in purchases)

    return {"total_purchase_amount": total}