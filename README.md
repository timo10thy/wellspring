Pharmacy Inventory Management System API

A backend Pharmacy Inventory Management System built with **FastAPI**, designed to help pharmacies manage products, monitor stock levels, track expiration dates, and handle sales operations with role-based access control.


Project Overview

This system allows pharmacies to efficiently manage inventory and sales operations with proper authorization control.

Admin Capabilities

* Add and manage products
* Add stock entries with expiry dates
* Monitor stock levels
* Track stock consumption
* Receive expiration alerts (180-day window)
* Manage users
* View sales records

User Capabilities

* View available products
* Sell products
* Automatically reduce stock upon sale


Tech Stack

* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Database Migrations:** Alembic
* **Authentication:** JWT-based authentication
* **Database:** PostgreSQL (Docker ready)
* **Containerization:** Docker & Docker Compose


Project Structure

```
.
├── alembic/                 
├── alembic.ini
├── app/
│   ├── auth/                 
│   ├── middlewares/          
│   ├── models/               
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── stock.py
│   │   ├── sales.py
│   │   └── enum.py
│   ├── routes/               
│   │   ├── auth.py
│   │   ├── user_route.py
│   │   ├── admin.py
│   │   ├── product.py
│   │   ├── stock.py
│   │   └── sales.py
│   ├── schema/               
│   ├── main.py               
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
```


Authentication & Roles

The system uses JWT authentication for secure access.

 Roles:

* **Admin**
* **User**

Admin-protected routes use dependency-based validation:


Core Features

Product Management

* Create new pharmacy products
* Update product details
* View product list

Stock Management

* Add stock entries per product
* Track stock quantity
* Monitor stock consumption
* Automatic deduction when sales occur


Expiration Alert System

The system checks for products expiring within **180 days**.

**Endpoint:**


GET /stocks/expiry-alerts


Expiry Classification Logic

| Days Remaining | Status               |
| -------------- | -------------------- |
| 90–180         | Warning              |
| 45–89          | Discount Recommended |
| 30–44          | Critical             |
| 1–29           | Very Critical        |
| ≤ 0            | Expired              |

Each alert includes:

* Product name
* Expiry date
* Remaining days
* Quantity affected
* Stock value (cost)
* Recommended action

Sales Management

* Users can sell products
* Stock reduces automatically
* Sales linked to:

  * Product
  * Stock batch
  * User who sold it


Installation Guide

Clone Repository

```bash
git clone <repository-url>
cd <project-folder>
```
Run With Docker

```bash
docker-compose up --build
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```
API Documentation

FastAPI automatically generates documentation.

* Swagger UI:

```
http://localhost:8000/docs
```
Database Migrations

Alembic is used for database version control.

Run migrations:

```bash
alembic upgrade head
```

Create new migration:

```bash
alembic revision --autogenerate -m "message"
```

---
Business Logic Highlights

* Batch-based stock management
* Expiry monitoring within 180 days
* Role-based route protection
* Relational mapping:

  * One product → Many stock entries
  * One stock → Many sales
  * One user → Many sales

Docker Support

The project includes:

* `Dockerfile`
* `docker-compose.yml`

For easy deployment and containerized database setup.


Future Improvements

* Dashboard analytics
* Pagination
* Reporting & export (CSV/PDF)
* Low-stock alerts
* Audit logs

Author

Timothy
Backend Developer 


