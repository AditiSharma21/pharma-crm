# Pharmacy CRM System

A full-stack Pharmacy Management CRM built using FastAPI (backend) and React (frontend).

---

## Tech Stack

Backend:
- Python
- FastAPI
- SQLAlchemy
- SQLite
- RESTful API architecture

Frontend:
- React (Functional Components + Hooks)
- Axios
- Responsive UI Layout

---

## Project Structure

```
/backend  → FastAPI REST API
/frontend → React application
```

---

## REST API Structure

### Inventory APIs
- GET /inventory
- POST /inventory
- PUT /inventory/{id}
- DELETE /inventory/{id}

Supports:
- Search by name
- Filter by status

---

### Sales APIs
- POST /sales
- GET /dashboard/today-sales
- GET /dashboard/total-items-sold
- GET /dashboard/recent-sales

---

### Purchase APIs
- POST /purchase-orders
- GET /dashboard/purchase-summary

---

## Data Consistency Logic

1. Stock Reduction Logic
When a sale is created:
- Medicine quantity is reduced.
- If insufficient stock → HTTP 400 error.
- Ensures transactional consistency.

2. Dynamic Status Detection
Medicine status is NOT permanently stored.
Instead, it is dynamically derived from quantity:

- quantity == 0 → Out of Stock
- quantity < 10 → Low Stock
- quantity >= 10 → Active

This avoids stale status data and ensures real-time correctness.

---

## Features

- Dashboard analytics
- Low stock detection
- Recent sales tracking
- Purchase summary
- Real API integration
- Loading & error states
- Clean card layout UI

---

## Running Locally

Backend:
```
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

Frontend:
```
cd frontend
npm install
npm start
```

---

## Live Deployment

Backend: Render  
Frontend: Vercel

---

## Author
Your Namegit init
git add .
git commit -m "Pharmacy CRM Submission"
git branch -M main
git remote add origin https://github.com/yourusername/pharmacy-crm.git
git push -u origin main